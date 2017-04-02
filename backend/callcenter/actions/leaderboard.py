from melenchonPB import redis
from accounts.models import User
from callcenter.models import UserExtend

def generateLeaderboards(top):

    alltime = generateLeaderboard('alltime', top)
    weekly = generateLeaderboard('weekly', top)
    daily = generateLeaderboard('daily', top)

    return alltime, weekly, daily

def generateLeaderboard(type, top):

    redisLeaderboard = redis.get_leaderboard(type, top)

    idList = [item[0] for item in redisLeaderboard]

    users = User.objects.filter(id__in=idList)

    leaderboard = []
    for ranked in redisLeaderboard:
        try:
            user = next(user for user in users if user.id==int(ranked[0]))
            username = user.UserExtend.agentUsername
            calls = int(ranked[1])
            leaderboard.append({'username': username, 'calls': calls})
        except User.DoesNotExist:
            pass
        except UserExtend.DoesNotExist:
            pass
        except StopIteration:
            pass

    return leaderboard