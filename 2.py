from django.db import models


class Player(models.Model):
    player_id = models.CharField(max_length=100)


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    title = models.CharField()


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()


def award_prize(player, level, prize):
    """
    Присвоение приза игроку за прохождение уровня.
    """
    # Проверяется, что игрок еще не получил этот приз
    if LevelPrize.objects.filter(player=player, level=level, prize=prize).exists():
        print("Player already has this prize for this level.")
        return
    # Создание и добавление приза для игрока
    new_prize = LevelPrize(player=player, level=level, prize=prize)
    new_prize.save()
    print(f"Awarded prize {prize} to player {player} for level {level}.")


# Для выгрузки в csv предположим, что наш главный проект носит имя app
from django.core import management

management.call_command('dumpdata',
                        'app.Player', fields=['player__player_id'],
                        'app.Level', fields=['level__title'],
                        'app.PlayerLevel', fields=['playerlevel__is_completed'],
                        'app.LevelPrize', fields=['levelPrize__prize'],
                        output='info.csv', indent=4)
