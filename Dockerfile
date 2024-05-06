
FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY ExtractionHandler.py ${LAMBDA_TASK_ROOT}
COPY RequestContext.py ${LAMBDA_TASK_ROOT}
COPY AWSInteraction ${LAMBDA_TASK_ROOT}/AWSInteraction
COPY extractors ${LAMBDA_TASK_ROOT}/extractors
#COPY mock_output.json ${LAMBDA_TASK_ROOT}/mock_output.json

# for tesseract
#RUN rpm -Uvh https://archives.fedoraproject.org//pub/archive//epel//4//x86_64//epel-release-4-10.noarch.rpm  
RUN rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

# for tesseract

RUN yum -y update
RUN yum -y install tesseract

CMD [ "lambda_function.lambda_handler" ]

