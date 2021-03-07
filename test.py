path = 'image.png'

last = path.split('/')[-1]
rest = '/'.join(path.split('/')[0:-1])

# print(last)
print(rest)

if rest == '':
    print('gay')


