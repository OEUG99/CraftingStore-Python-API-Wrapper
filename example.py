from csaw import CSAW


client = CSAW()

csaw = client.auth('NjJDwRXmo0wEZ80IaUyu6xERDtK6vrrA0QI1mb2s3Ajj6vXbUT')
gc = csaw.create_giftcard(10)
print(gc.id)
print(csaw.get_giftcard(gc.id))

print('test')