from django.db import models
from django.contrib.postgres.fields import ArrayField


class QuestionBlock(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    question_list = ArrayField(models.IntegerField(), null=True)
    question_group_list = ArrayField(models.IntegerField(), null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'question_block'


class QuestionGroup(models.Model):
    question_list = ArrayField(models.IntegerField())

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'question_group'


class Question(models.Model):
    author = models.IntegerField()
    role_of_author = models.CharField(default="anonym")

    STATUS_TYPES = (
        ('public', 'public'),
        ('custom', 'custom'),
        ('draft', 'draft')
    )
    status = models.CharField(choices=STATUS_TYPES)

    QUESTION_TYPES = (
        ('table', 'table'),
        ('upload_link', 'upload_link'),
        ('upload_file', 'upload_file'),
        ('select_list', 'select_list'),
        ('date', 'date'),
        ('text', 'text'),
        ('numeric_with_measurement_unit', 'numeric_with_measurement_unit'),
        ('numeric', 'numeric'),
        ('toggle', 'toggle'),
    )
    question_type = models.CharField(choices=QUESTION_TYPES)

    DATA_TYPES = (
        ('medical', 'medical'),
        ('non-medical', 'non-medical'),
        ('clarifying', 'clarifying')
    )
    data_type = models.CharField(choices=DATA_TYPES)
    question_value = models.TextField()
    question_label = models.TextField(null=True)
    prompt_text = models.TextField(null=True)
    required_answer = models.BooleanField(default=False)
    allow_multiple_answer = models.BooleanField(default=False)
    historically_tracked = models.BooleanField(default=False)
    parent_question_id = models.IntegerField(null=True)  # only clarifying
    answer_values = ArrayField(models.CharField(max_length=128), null=True)  # only toggle
    multiple_selection = models.BooleanField(default=False)  # only select_list
    min_additions = models.IntegerField(null=True)  # only upload file/link
    max_additions = models.IntegerField(null=True)  # only upload file/link
    min_symbols = models.IntegerField(null=True)  # only text
    max_symbols = models.IntegerField(null=True)  # only text
    rows_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6')
    )
    rows_number = models.CharField(choices=rows_choices, default="2")  # only text
    keywords_recognize = models.BooleanField(default=False)  # only text
    date_type = models.CharField(choices=(('one', 'one'), ("start_and_end", "start_and_end")), null=True)  # only date
    allow_current_future_date = models.BooleanField(default=False)  # only date
    allow_approximate_date = models.BooleanField(default=False)  # only date
    measurement_units = models.CharField(max_length=128, null=True)  # numeric with Measurement
    measurement_unit_by_default = models.CharField(null=True)  # numeric with Measurement

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'question'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'answer'


class Chapter(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    question_list = ArrayField(models.IntegerField(), null=True)
    question_group_list = ArrayField(models.IntegerField(), null=True)
    question_block_list = ArrayField(models.IntegerField(), null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'chapter'


class Questionnarie(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    question_list = ArrayField(models.IntegerField(), null=True)
    question_group_list = ArrayField(models.IntegerField(), null=True)
    question_block_list = ArrayField(models.IntegerField(), null=True)
    chapter_list = ArrayField(models.IntegerField(), null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'questionnarie'