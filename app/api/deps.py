from typing import Annotated

from fastapi import Depends

from app.core.s3 import ReplayS3Service, get_replay_s3_service

S3ServiceDep = Annotated[ReplayS3Service, Depends(get_replay_s3_service)]
