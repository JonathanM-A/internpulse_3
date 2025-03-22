from .base import *
from .base import env

SECRET_KEY = env(
    "TEST_SECRET_KEY", default="s1*du$i#bw&2_shl7v!e1%naw38g5(z!h-f@q*n)g-j8@!^&i2"
)