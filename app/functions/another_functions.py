async def get_answer_calories(data):
    voo: float
    calories: float
    target: bool
    if isinstance(data, dict):
        voo = (10 * float(data["weight"]) + 6.25 * int(data["growth"])
               - 5 * int(data["age"]) - (0 if data["male"] else 161))
        calories = voo * float(data["activity"])
        target = bool(data["target"])
    else:
        voo = (10 * float(data.weight) + 6.25 * int(data.growth)
               - 5 * int(data.age) - (0 if data.male else 161))
        calories = voo * float(data.activity)
        target = bool(data.target)

    print(f"{voo=}, {calories=}")
    belki = calories * 0.20
    sddp_belki = belki * 0.30
    jiri = calories * 0.30
    sddp_jiri = jiri * 0.05
    yglevodi = calories * 0.50
    sddp_yglevodi = yglevodi * 0.05
    sddp = sddp_belki + sddp_jiri + sddp_yglevodi

    print(f"{belki=}, {sddp_belki=}")
    print(f"{jiri=}, {sddp_jiri=}")
    print(f"{yglevodi=}, {sddp_yglevodi=}")
    print(f"{sddp=}")

    calories += sddp
    print(f"calories + sddp = {calories}")

    res = str()
    res += f"Ваша суточная норма калорий: {int(calories)} калорий\n"
    if target:
        res += f"Но для набора массы необходимо делать профицит хотя бы на 10%: {int(calories * 1.1)} калорий\n"
        res += (f"Белки: {int((belki + sddp_belki) * 1.1 // 4)}\n"
                f"Жиры: {int((jiri + sddp_jiri) * 1.1 // 9)}\n"
                f"Углеводы: {int((yglevodi + sddp_yglevodi) * 1.1 // 4)}")
    else:
        res += f"Но для снижения веса необходимо делать дефицит хотя бы на 10%: {int(calories * 0.9)} калорий\n"
        res += (f"Белки: {int((belki + sddp_belki) * 0.9 // 4)}\n"
                f"Жиры: {int((jiri + sddp_jiri) * 0.9 // 9)}\n"
                f"Углеводы: {int((yglevodi + sddp_yglevodi) * 0.9 // 4)}")

    return res
