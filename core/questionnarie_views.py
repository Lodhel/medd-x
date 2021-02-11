from models import QuestionBlock
from models import QuestionGroup
from models import Question
from models import Chapter
from models import Questionnarie


class QuestionView:
    async def post(self, data):
        instance = await Question(**data)
        instance.create()

        return instance