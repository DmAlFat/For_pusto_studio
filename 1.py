from django.db import models

import datetime


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    # Поле для учёта последней даты входа игрока, а также для отслеживания даты первого входа
    last_entry_date = models.DateTimeField(auto_now_add=True)
    # Поле для учёта баллов за ежедневный вход
    daily_score = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Boost(models.Model):
    boost_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    boost_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Связь между игроком и бустами
class PlayerBoosts(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    boost = models.ForeignKey(Boost, on_delete=models.CASCADE)
    start_date = models.DateTimeField()  # Дата начала действия буста
    end_date = models.DateTimeField(null=True)  # Дата окончания действия буста

    class Meta:
        unique_together = ('player', 'boost')

    def __str__(self):
        return f"{self.player}: {self.boost}"

    # Метод для обновления баллов за ежедневный вход
    def update_daily_score(player, current_datetime):
        last_entry_date = player.last_entry_date  # Получение последней даты входа игрока
        if last_entry_date == current_datetime:
            return  # Если текущая дата совпадает с последней датой входа игрока, то метод завершается
        player.last_entry_date = current_datetime  # Обновление даты последнего входа игрока
        player.daily_score += 50  # Предположим, что за ежедневный вход начисляется 50 "очков"
        player.save()

    # Метод для начисления бустов
    def award_boost(player, boost_type):
        try:
            boost = Boost.objects.get(type=boost_type)
        except Boost.DoesNotExist:
            raise ValueError(f"Boost with type '{boost_type}' does not exist.")
        # Проверка на наличие данного буста у игрока
        if PlayerBoosts.objects.filter(player=player, boost=boost).exists():
            print("Player already has this boost.")
            return
        # Создание нового буста для игрока
        new_boost = PlayerBoosts(player=player, boost=boost)
        new_boost.save()
        print(f"Awarded boost {boost} to player {player}.")
