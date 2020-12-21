"""
You reach the train's last stop and the closest you can get to your vacation island without getting wet. There aren't even any boats here, but nothing can stop you now: you build a raft. You just need a few days' worth of food for your journey.

You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens are listed in a language you do understand. You should be able to use this information to determine which ingredient contains which allergen and work out which foods are safe to take with you on your trip.

You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's ingredients list followed by some or all of the allergens the food contains.

Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list), the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list. However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present: maybe they forgot to label it, or maybe it was labeled in a language you don't know.

For example, consider the following list of foods:

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)

could be fish = sqjcc mxmxvkd
could be dairy = mxmxvkd 
could be soy = sqjhc fvjkl

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
The first food in the list has four ingredients (written in a language you don't understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food might contain other allergens, a few allergens the food definitely contains are listed afterward: dairy and fish.

The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list. In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen. Counting the number of times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which appears twice.

Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those ingredients appear?    

--- Part Two ---
Now that you've isolated the inert ingredients, you should have enough information to figure out which ingredient contains which allergen.

In the above example:

mxmxvkd contains dairy.
sqjhc contains fish.
fvjkl contains soy.
Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your canonical dangerous ingredient list. (There should not be any spaces in your canonical dangerous ingredient list.) In the above example, this would be mxmxvkd,sqjhc,fvjkl.

Time to stock your raft with supplies. What is your canonical dangerous ingredient list?
"""


from collections import defaultdict
if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    all_ingredients = set()
    all_allergens = set()
    food_ingredients = []
    food_allergens = []

    # Parse input
    for line in lines:
        ing_str, all_str = line.split(" (contains ")
        all_str = all_str[:-1]
        ingredients = set(ing_str.split(" "))
        allergens = set(all_str.split(", "))
        all_ingredients.update(ingredients)
        food_ingredients.append(ingredients)
        food_allergens.append(allergens)
        all_allergens.update(allergens)

    could_have_allergen = defaultdict(lambda: all_ingredients)

    # Since only one ingredient can have each allergen the only ingredients that could have an allergen
    # are in the intersection of the ingredients lists that list that allergen
    for i, ingredients_set in enumerate(food_ingredients):
        for allergen in food_allergens[i]:
            could_have_allergen[allergen] = could_have_allergen[allergen].intersection(ingredients_set)

    # Find all ingredients that aren't in an allergen set
    remaining_ingredents = all_ingredients
    for allergen, ingredient_set in could_have_allergen.items():
        remaining_ingredents -= ingredient_set

    # Find number of appearances for ingredients without allergens
    appearance_ct = 0
    for ingredient in remaining_ingredents:
        for ingredient_set in food_ingredients:
            if ingredient in ingredient_set:
                appearance_ct += 1
    print("Answer1:",  appearance_ct)

    # Part 2
    # Find ingredient - allergen assignments
    # If only one ingredient could have a given allergen we remove that ingredient from all other sets
    # Repeat until we (hopefully) have one ingredient in each allergen set
    assigned = set()
    while assigned != all_allergens:
        for allergen in could_have_allergen:
            ingredient_set = could_have_allergen[allergen]
            if len(ingredient_set) == 1:
                ingredient = list(ingredient_set)[0]
                assigned.add(allergen)
                for other_allergen in could_have_allergen:
                    if allergen != other_allergen:
                        could_have_allergen[other_allergen] -= {ingredient}

    # Sort ingredients by allergen alphabetically
    ingredients = [list(could_have_allergen[allergen])[0] for allergen in sorted(could_have_allergen)]
    print("Answer2:", ",".join(ingredients))