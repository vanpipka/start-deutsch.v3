from django.db.models import Count
from ..models import Test, TestsCountByLevelTypePart, ExamLevel, TestCategory, TestPart


def rebuild_test_counters():

    # 1. Удаляем старые данные
    TestsCountByLevelTypePart.objects.all().delete()

    # 2. Получаем агрегированную статистику
    stats = (
        Test.objects
        .values("exam__level", "exam__category", "part")
        .annotate(count=Count("id"))
    )

    # превращаем в dict для быстрого поиска
    stats_map = {
        (
            row["exam__level"],
            row["exam__category"],
            row["part"],
        ): row["count"]
        for row in stats
    }

    # 3. Берём ВСЕ возможные значения
    levels = ExamLevel.objects.all()
    categories = TestCategory.objects.all()
    parts = TestPart.objects.all()

    objs = []

    # 4. Создаём ВСЕ комбинации
    for level in levels:
        for category in categories:
            for part in parts:

                if part.level != level:
                    continue
                if part.category != category:
                    continue
                
                count = stats_map.get((level.id, category.id, part.id), 0)

                objs.append(
                    TestsCountByLevelTypePart(
                        level=level,
                        category=category,
                        part=part,
                        count=count,
                    )
                )

    # 5. Массовая вставка
    TestsCountByLevelTypePart.objects.bulk_create(objs)