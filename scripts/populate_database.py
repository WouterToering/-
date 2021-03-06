# lazy, use: python manage.py shell < scripts/populate_database.py

from apps.workout_tracker.models import *  # noqa

# Delete potential old data
Exercise.objects.all().delete()
ExerciseType.objects.all().delete()
Workout.objects.all().delete()
Week.objects.all().delete()
Program.objects.all().delete()

program = Program(name='Lvysaur 4-4-8 for beginners')
program.save()

weeks = dict(
    a=Week(name='Week A', program_id=program.id, position=0),
    b=Week(name='Week B', program_id=program.id, position=1)
)

_ = [o.save() for _, o in weeks.items()]

exercise_types = dict(
    bench=ExerciseType(name='Bench press', weight_progression=5),
    squat=ExerciseType(name='Squat', weight_progression=7.5),
    dl=ExerciseType(name='Deadlift', weight_progression=7.5),
    row=ExerciseType(name='Barbell row', weight_progression=7.5),
    ohp=ExerciseType(name='Overhead press', weight_progression=2.5),
    chinup=ExerciseType(name='Chinup', weight_progression=0)
)


_ = [o.save() for _, o in exercise_types.items()]

workouts_week_a = dict(
    day_1=Workout(week_id=weeks['a'].id, name='Day 1', position=0),
    day_2=Workout(week_id=weeks['a'].id, name='Day 2', position=1),
    day_3=Workout(week_id=weeks['a'].id, name='Day 3', position=2),
)

workouts_week_b = dict(
    day_1=Workout(week_id=weeks['b'].id, name='Day 1', position=0),
    day_2=Workout(week_id=weeks['b'].id, name='Day 2', position=1),
    day_3=Workout(week_id=weeks['b'].id, name='Day 3', position=2),
)

whatever = {'a': workouts_week_a, 'b': workouts_week_b}

_ = [o.save() for _, o in workouts_week_a.items()]
_ = [o.save() for _, o in workouts_week_b.items()]


bla = {
    'a': {
        'day_1': [
            ['bench', 4, 4],
            ['squat', 4, 8],
            ['ohp', 4, 8],
            ['chinup', 4, 8],
        ],
        'day_2': [
            ['bench', 4, 8],
            ['dl', 4, 4],
            ['ohp', 4, 4],
            ['row', 4, 8],
        ],
        'day_3': [
            ['bench', 3, 4],
            ['squat', 3, 4],
            ['ohp', 4, 8],
            ['row', 4, 4],
        ]
    },
    'b': {
        'day_1': [
            ['bench', 4, 8],
            ['dl', 4, 8],
            ['ohp', 4, 4],
            ['row', 4, 4],
        ],
        'day_2': [
            ['bench', 4, 4],
            ['squat', 4, 8],
            ['ohp', 4, 8],
            ['chinup', 4, 8],
        ],
        'day_3': [
            ['bench', 4, 8],
            ['dl', 3, 4],
            ['ohp', 3, 4],
            ['row', 4, 8],
        ]
    }
}


for week, days in sorted(bla.items(), key=lambda x: x[0]):
    week_obj = weeks[week]

    for day, exercise_lists in sorted(days.items(), key=lambda x: x[0]):
        workout_obj = whatever[week][day]

        i = 0

        for exercise_list in exercise_lists:
            exercise_name, sets, reps = exercise_list
            exercise_type_obj = exercise_types[exercise_name]

            kwargs = {
                'workout_id': workout_obj.id,
                'exercise_type_id': exercise_type_obj.id,
                'weight_multiplier': 1,
                'position': i
            }

            if reps == 8:
                kwargs['weight_multiplier'] = 0.9

            Exercise(**kwargs, sets=sets, reps=reps).save()

            if sets == 3:
                i += 1
                kwargs['is_amrap'] = True
                kwargs['position'] = i
                Exercise(**kwargs).save()

            i += 1
