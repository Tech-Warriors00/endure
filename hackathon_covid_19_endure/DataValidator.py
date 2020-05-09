# this class is used to evalute phone, etc. which are provided by the user before sending the data into
# database


def validatePhone(phone):
    # checks entered phone number is 10 digit numerical value or not

    if phone.__len__() == 10:
        print('yay')
        # step 2: convert to int() type; if converted then phone is numeric else non-numeric

        try:
            pin = int(phone)  # phone is numeric
            print('True')
            return 'True'
        except:
            print('invalid phone number')
            return 'invalid phone number'
    else:
        print('invalid phone number')
        return 'invalid phone number'


def validateEmail(email):
    # checks entered email that it has only one '@' symbol

    count = email.count("@")
    if count == 1:
        print('valid email')
        return 'True'
    else:
        print('invalid email')
        return 'invalid email'


def matchPasswords(password, confirmPassword):
    if password == confirmPassword:
        return 'True'
    else:
        return 'Passwords did not match'
