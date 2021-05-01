def myToken(func):
    def wrapper(token):
        if token != '123456':
            print(3)
            print({'Error': 'Please Login First'})
        elif token == '123456':
            func(token)
            print('欢迎~~~')

    return wrapper


@myToken
def test():
    print('token')


if __name__ == '__main__':
    test('123456')