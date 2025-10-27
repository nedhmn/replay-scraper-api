import json
import logging
from typing import Any

import aioboto3
from botocore.exceptions import ClientError
from fastapi import Request

from app.core.config import settings

logger = logging.getLogger(__name__)


class ReplayS3Service:
    def __init__(self, session: aioboto3.Session):
        self.session = session
        self.bucket_name = settings.S3_BUCKET_NAME
        self.prefix = settings.S3_REPLAYS_PREFIX
        self.region = settings.AWS_REGION

    def _get_s3_key(self, replay_id: str) -> str:
        return f"{self.prefix}{replay_id}_replay.json"

    async def get_replay(self, replay_id: str) -> dict[str, Any] | None:
        s3_key = self._get_s3_key(replay_id)

        async with self.session.client("s3", region_name=self.region) as s3_client:
            try:
                logger.info("Checking S3 for replay: %s", s3_key)
                response = await s3_client.get_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                )

                body_bytes = await response["Body"].read()
                replay_data: dict[str, Any] = json.loads(body_bytes.decode("utf-8"))

                logger.info("Found replay in S3: %s", s3_key)
                return replay_data

            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "NoSuchKey":
                    logger.info("Replay not found in S3: %s", s3_key)
                    return None

                logger.error(
                    "S3 error retrieving replay %s: %s - %s",
                    s3_key,
                    error_code,
                    e.response["Error"]["Message"],
                )
                raise

    async def save_replay(self, replay_id: str, data: dict[str, Any]) -> None:
        s3_key = self._get_s3_key(replay_id)

        async with self.session.client("s3", region_name=self.region) as s3_client:
            try:
                logger.info("Saving replay to S3: %s", s3_key)

                json_bytes = json.dumps(data, indent=2).encode("utf-8")

                await s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=json_bytes,
                    ContentType="application/json",
                )

                logger.info("Successfully saved replay to S3: %s", s3_key)

            except ClientError as e:
                logger.error(
                    "S3 error saving replay %s: %s - %s",
                    s3_key,
                    e.response["Error"]["Code"],
                    e.response["Error"]["Message"],
                )
                raise


def get_replay_s3_service(request: Request) -> ReplayS3Service:
    session = request.app.state.aioboto3_session
    return ReplayS3Service(session)
