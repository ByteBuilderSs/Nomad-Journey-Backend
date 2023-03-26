from django.db import models
from accounts.models import User
from django.utils.translation import gettext as _



class Announcement(models.Model):
    ONE_TR = 1
    TWO_TR = 2
    THREE_TR = 3
    FOUR_TR = 4
    FIVE_TR = 5
    SIX_TR = 6
    SEVENT_TR = 7
    EIGHT_TR = 8
    NINE_TR = 9
    TEN_TR = 10
    ELEVEN_TR = 11
    TWELVE_TR = 12
    THIRTEEN_TR = 13
    FOURTEEN_TR = 14
    FIFTEEN_TR = 15
    TRAVELERS_COUNT_CHOICES = [
        (ONE_TR, _("1")),
        (TWO_TR, _("2")),
        (THREE_TR, _("3")),
        (FOUR_TR, _("4")),
        (FIVE_TR, _("5")),
        (SIX_TR, _("6")),
        (SEVENT_TR, _("7")),
        (EIGHT_TR, _("8")),
        (NINE_TR, _("9")),
        (TEN_TR, _("10")),
        (ELEVEN_TR, _("11")),
        (TWELVE_TR, _("12")),
        (THIRTEEN_TR, _("13")),
        (FOURTEEN_TR, _("14")),
        (FIFTEEN_TR, _("15"))
    ]
    announcer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None
    )

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    arrival_date_is_flexible = models.BooleanField(null=True)
    departure_date_is_flexible = models.BooleanField(null=True)
    message = models.TextField(max_length=500, null=True)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    travelers_count = models.IntegerField(choices=TRAVELERS_COUNT_CHOICES, null=True, blank=True)

    def __str__(self):
        return 'This is an announcement with ID ' + str(self.id) + '.'
