import datetime

from .question_models import *


class Profile(models.Model):
    token = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    is_step = models.BooleanField(default=False)
    is_send = models.BooleanField(default=False)
    is_sms = models.BooleanField(default=True)
    is_email = models.BooleanField(default=True)
    check = models.DateTimeField(default=datetime.datetime.today())
    date_joined = models.DateTimeField(default=datetime.datetime.today())
    email = models.EmailField(max_length=32, null=True)
    phone = models.CharField(max_length=16, null=True)
    sms_code = models.CharField(max_length=4, null=True)
    LANG_CHOICES = (
        ('en', 'en'),
        ('de', 'de'),
        ('fr', 'fr'),
        ('sp', 'sp'),
        ('ru', 'ru'),
        ('pt', 'pt'),
        ('it', 'it'),
        ('ja', 'ja'),
        ('ko', 'ko'),
        ('zh', 'zh'),
        ('tr', 'tr'),
    )
    language = models.CharField(max_length=2, choices=LANG_CHOICES, default="en")
    country = models.CharField(max_length=64, default="Russia")
    city = models.CharField(max_length=64, default="Moscow")

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'profile'


class Company(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    COMPANY_TYPES = (
        ('Clinic', 'Clinic'),
        ('Insurance company', 'Insurance company'),
        ('Medtravel company', 'Medtravel company'),
        ('Pharmaceutical company', 'Pharmaceutical company'),
        ('Charity foundation', 'Charity foundation')
    )
    type_c = models.CharField(max_length=64, choices=COMPANY_TYPES, default="Clinic")
    name = models.CharField(max_length=64, null=True)
    step = models.IntegerField(default=0)
    representatives_phones = ArrayField(
        models.CharField(max_length=32),
        null=True
    )
    representatives_emails = ArrayField(
        models.EmailField(max_length=64),
        null=True
    )

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'company'
        verbose_name = 'company'
        verbose_name_plural = 'companies'


class Anonym(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    cover_name = models.CharField(max_length=64, null=True)
    step = models.IntegerField(default=0)

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'anonym'
        verbose_name = 'anonym-patient'
        verbose_name_plural = 'anonym-patients'


class Secure(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    questionary = models.TextField()
    step = models.IntegerField(default=0)

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'secure'
        verbose_name = 'secure-patient'
        verbose_name_plural = 'secure-patients'


class Manager(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    middle_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    step = models.IntegerField(default=0)

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'manager'
        verbose_name = 'company manager'
        verbose_name_plural = 'company managers'


class Physician(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    middle_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    step = models.IntegerField(default=0)

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'physician'


class Assistant(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    middle_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    step = models.IntegerField(default=0)

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'assistant'


class Translator(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    middle_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    step = models.IntegerField(default=0)

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'translator'


class Cookie(models.Model):
    title = models.CharField(max_length=255)
    date_check = models.DateTimeField(default=datetime.datetime.today())
    data = ArrayField(
        models.TextField(),
        null=True
    )
    src = models.URLField()

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'cookie'


class ReferenceBook(models.Model):
    title = models.CharField(max_length=255)
    let = models.BooleanField(default=True)
    default_columns = ArrayField(models.CharField(max_length=255))

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'reference_book'


class UserChoicesRB(models.Model):
    rb = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE)
    column = models.CharField(max_length=255)
    status = models.BooleanField(default=False)