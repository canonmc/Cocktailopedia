class Cocktail:
    def __init__(self, name,  *args):
        self.name = name
        self.ingredients = dict([])
        for item,amount,unit in args:
            self.ingredients[item.lower()] = (amount,unit.lower())

    def __str__(self):
        ans = self.name + "\n"
        for i,j in self.ingredients.items():
            ans += f'{j[0]}  {j[1]} of {i}\n'
        return ans