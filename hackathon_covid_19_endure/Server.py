from flask import Flask, request, Response
from flask_restful import Resource, Api

import DatabaseConnection as batch
import DataValidator as validate
from ConvertMessageToJSON import toJsonFormat as asJson

app = Flask(__name__)
api = Api(app)


class RegisterUser(Resource):
    def post(self, name, address, phone, email, password, confirmPassword):
        # this function is used to insert user's record in the database
        print('inside Register.post()...')

        name = name.strip().lower()
        address = address.strip().lower()
        phone = phone.strip().lower()
        email = email.strip().lower()

        # check phone
        isPhoneValid = validate.validatePhone(phone)

        print('phone', isPhoneValid)
        if isPhoneValid == 'True':
            # check email
            isEmailValid = validate.validateEmail(email)

            print('email', isEmailValid)
            if isEmailValid == 'True':
                # match passwords
                isPasswordMatched = validate.matchPasswords(password, confirmPassword)

                print('password', isPasswordMatched)
                if isPasswordMatched == 'True':
                    # all found correct. Now, insert into database
                    isInserted = batch.insertIntoUser(name, address, phone, email, password)

                    print('inserted', isInserted)
                    if isInserted == "Verification code has been sent to your email address. Check your email " \
                                     "and enter the code.":
                        return asJson("Verification code has been sent to your email address. Check your email and "
                                      "enter the code.")
                    else:
                        return asJson(isInserted)
                else:
                    return asJson(isPasswordMatched)
            else:
                return asJson(isEmailValid)
        else:
            return asJson(isPhoneValid)


class RegisterOwner(Resource):
    def post(self, name, shop_type, shop_name, address, phone, email, password, confirmPassword, mon, tue, wed,
             thu, fri, sat, sun, b1, b2, b3, b4):
        # this function is used to insert owner's record in the database
        print('inside Register.post()...')

        name = name.strip().lower()
        shop_type = shop_type.strip().lower()
        shop_name = shop_name.strip().lower()
        address = address.strip().lower()
        phone = phone.strip().lower()
        email = email.strip().lower()
        mon = mon.strip()
        tue = tue.strip()
        wed = wed.strip()
        thu = thu.strip()
        fri = fri.strip()
        sat = sat.strip()
        sun = sun.strip()
        b1 = b1.strip()
        b2 = b2.strip()
        b3 = b3.strip()
        b4 = b4.strip()

        # check phone
        isPhoneValid = validate.validatePhone(phone)

        print('phone', isPhoneValid)
        if isPhoneValid == 'True':
            # check email
            isEmailValid = validate.validateEmail(email)

            print('email', isEmailValid)
            if isEmailValid == 'True':
                # match passwords
                isPasswordMatched = validate.matchPasswords(password, confirmPassword)

                print('password', isPasswordMatched)
                if isPasswordMatched == 'True':
                    # all found correct. Now, insert into database
                    isInserted = batch.insertIntoOwner(name, shop_type, shop_name, address, phone, email, password,
                                                       mon, tue, wed, thu, fri, sat, sun, b1, b2, b3, b4)

                    print('inserted', isInserted)
                    if isInserted == "Verification code has been sent to your email address. Check your email " \
                                     "and enter the code.":
                        return asJson("Verification code has been sent to your email address. Check your email and "
                                      "enter the code.")
                    else:
                        return asJson(isInserted)
                else:
                    return asJson(isPasswordMatched)
            else:
                return asJson(isEmailValid)
        else:
            return asJson(isPhoneValid)


# this class is used to set `is_account_active` = 1 and `is_verified` = 1;
# called when 'Confirm Verification' button is pressed
class Activation(Resource):
    def post(self, of, email, otp):
        """
        :param of: 'user' or 'owner'
        """
        of = of.strip().lower()
        email = email.strip().lower()
        otp = otp.strip()

        # check email
        isEmailValid = validate.validateEmail(email)

        if isEmailValid == 'True':
            isVerified = batch.verifyCode(of, email, otp)
            return asJson(isVerified)
        else:
            return asJson(isEmailValid)


def atStarting():  # call this function at the very beginning
    batch.start()


# class to login user/owner and set `is_active` = 1
class Login(Resource):
    def get(self, of, email, password):
        """:param of: 'user' or 'owner'
        """

        of = of.strip().lower()
        email = email.strip().lower()

        # check email
        isEmailValid = validate.validateEmail(email)
        if isEmailValid == 'True':
            isCorrect = batch.login(of, email, password)
            if isCorrect == 'True':
                print('You are logged in')
                return asJson(True)
            else:
                return asJson(isCorrect)
        else:
            return asJson(isEmailValid)


class UpdateUserInfo(Resource):
    def put(self, email, name, address, phone):
        email = email.strip().lower()  # cannot be updated
        name = name.strip().lower()
        address = address.strip().lower()
        phone = phone.strip()

        # check phone
        isPhoneValid = validate.validatePhone(phone)

        if isPhoneValid is True:
            # update data
            return asJson(batch.updateUser(email, name, address, phone))
        else:
            return asJson(isPhoneValid)


class UpdateOwnerInfo(Resource):
    def put(self, email, name, shop_type, shop_name, address, phone, mon, tue, wed, thu, fri, sat, sun,
            b1, b2, b3, b4):
        email = email.strip().lower()
        name = name.strip().lower()
        shop_type = shop_type.strip().lower()
        shop_name = shop_name.strip().lower()
        address = address.strip().lower()
        phone = phone.strip()
        mon = mon.strip()
        tue = tue.strip()
        wed = wed.strip()
        thu = thu.strip()
        fri = fri.strip()
        sat = sat.strip()
        sun = sun.strip()
        b1 = b1.strip()
        b2 = b2.strip()
        b3 = b3.strip()
        b4 = b4.strip()

        # check phone
        if validate.validatePhone(phone) != 'True':
            return asJson(validate.validatePhone(phone))

        # update
        return asJson(batch.updateOwner(email, name, shop_type, shop_name, address, phone, mon, tue, wed, thu, fri,
                                 sat, sun, b1, b2, b3, b4))


class CustomerList(Resource):
    def get(self, address):
        address = address.strip().lower()

        return batch.getCustomersInLocality(address)


class ShopsInLocalityOfSameCategory(Resource):
    def get(self, shopType, address):
        shopType = shopType.strip().lower()
        address = address.strip().lower()

        return batch.getShopsInLocalityOfSameOrNotCategory(shopType, address)


class ShopsInSameLocality(Resource):
    def get(self, address):
        address = address.strip().lower()

        return batch.getShopsInLocalityOfSameOrNotCategory(None, address)


class DeactivateAccount(Resource):
    def put(self, of, email):
        """
        :param of: 'owner' or 'user'
        """
        of = of.strip().lower()
        email = email.strip().lower()

        return asJson(batch.deactivateAccount(of, email))


class IssueComplaint(Resource):
    def post(self, issuedBy, issuedTo, reason):
        issuedBy = issuedBy.strip().lower()
        issuedTo = issuedTo.strip().lower()
        reason = reason.strip().lower()

        return asJson(batch.issueComplaint(issuedBy, issuedTo, reason))


class ComplaintIssuedAgainstMe(Resource):
    def get(self, email):
        email = email.strip().lower()

        return batch.getComplaintIssuedAgainstMe(email)


class BatchAllotment(Resource):
    def get(self, address, shopType, date):
        address = address.strip().lower()
        shopType = shopType.strip().lower()
        date = date.strip()  # format: YYYY-MM-DD
        return asJson(batch.batchAllotment(address, shopType, date))


class ShopsOfSameBatch(Resource):
    def get(self, email):
        email = email.strip().lower()

        return batch.getShopsOfSameBatch(email)


class BatchAllotmentDetails(Resource):
    def get(self, email, tense):
        """
        :param tense: 'past', 'present' or 'future'
        """
        tense = tense.strip().lower()
        email = email.strip().lower()

        return batch.getBatchAllotmentDetails(email, tense)


class ShopDetails(Resource):
    def get(self, email):
        email = email.strip().lower()

        return batch.getShopDetails(email)


class About(Resource):
    def get(self):
        idea = "We all are well aware of the fact that its very crucial time that we are going through due to " \
               "COVID 19 pandemic. As per the goverment rule its very important to follow the lockdown. But due " \
               "to the extension of the lockdown businessmen and shopkeepers are facing problem as they are " \
               "becoming financially weak with every passing day." \
               "Government has given permission only to a handful of shop's to be kept open. This lockdown " \
               "is mainly affecting retailers, daily laborers and other shop-domains like furniture, " \
               "stationary, toy shops, cafe's etc. These people also need to have a strong financial backbone. " \
               "Here, complete lockdown is not a solution and giving permission to open all shops is also not " \
               "a solution. As it will lead to massive failure of SOCIAL-DISTANCING. " \
               "So my team came up with a mid-way solution both for retailers and the government, we have " \
               "named it Endure! Here we are developing an automated batch-allotment system which will " \
               "allot batches to shopkeeper's as per decision of Government authorities. It will help " \
               "retailers to do business it an efficient, smooth and discipined manner. Shopkeeper's need " \
               "to signup in our App and choose their working days plus their preference batches. Shops " \
               "will be allotted batches in which they have to be opened. Batches will be given according " \
               "to address and shop type, and will be issued by government itself. The system will allot " \
               "batches according to preferences and minimum number of shops should be opened per-batch in " \
               "order to reduce traffic in the roads and follow SOCIAL-DISTANCING. Customer's can view shop " \
               "opening and closing time from their interface. And most importantly uniform functioning time " \
               "will be given to each shop (which will lead to equal opportunity for all shopkeeper's " \
               "to earn). And all batches will be uniformly filled so that there is no unavailability of " \
               "resources to the customer from 6:00 AM to 10:00 PM for any given day. " \
               "As Endure will be a government shop-monitoring and batch-allotment app so if a user doesn't " \
               "open his/her shop for the given batch then the customer's can file a complaimt againt the " \
               "shopkeeper. And if shopkeeper keeps his/her shop open on invalid batches then other " \
               "shopkeeper's can also file a complaint against that shop. Complaints can be registered " \
               "by nearby police-stations. " \
               "Not only will it help to reduce panic among shop-keepers but will also give opportunity " \
               "to shopkeepers to earn. And also help reducing roaming of people in search of commodities " \
               "as they will be well aware which shop is going to opened at what time. This project can be " \
               "continued as a token-booking system for customer's. As customer's can book their slot when " \
               "the shop is opened. " \
               "A small step to make the Indian economy strong once again."
        return asJson(idea)


# api(s)
api.add_resource(RegisterUser, '/signup/user/<string:name>/<string:address>/<string:phone>/<string:email>/'
                               '<string:password>/<string:confirmPassword>')
api.add_resource(RegisterOwner, '/signup/owner/<string:name>/<string:shop_type>/<string:shop_name>/<string:address>/'
                                '<string:phone>/<string:email>/<string:password>/<string:confirmPassword>/'
                                '<string:mon>/<string:tue>/<string:wed>/<string:thu>/<string:fri>/<string:sat>/'
                                '<string:sun>/<string:b1>/<string:b2>/<string:b3>/<string:b4>')
api.add_resource(Activation, '/activate/<string:of>/<string:email>/<string:otp>')
api.add_resource(Login, '/login/<string:of>/<string:email>/<string:password>')
api.add_resource(UpdateUserInfo, '/update/user/<string:email>/<string:name>/<string:address>/<string:phone>')
api.add_resource(UpdateOwnerInfo, '/update/owner/<string:email>/<string:name>/<string:shop_type>/'
                                  '<string:shop_name>/<string:address>/<string:phone>/<string:mon>/'
                                  '<string:tue>/<string:wed>/<string:thu>/<string:fri>/<string:sat>/'
                                  '<string:sun>/<string:b1>/<string:b2>/<string:b3>/<string:b4>')
api.add_resource(CustomerList, '/nearby/customers/<string:address>')
api.add_resource(ShopsInLocalityOfSameCategory, '/nearby/shops/same_category/<string:shopType>/<string:address>')
api.add_resource(ShopsInSameLocality, '/nearby/shops/all_category/<string:address>')
api.add_resource(DeactivateAccount, '/deactivate/<string:of>/<string:email>')
api.add_resource(IssueComplaint, '/complaint/issue/<string:issuedBy>/<string:issuedTo>/<string:reason>')
api.add_resource(ComplaintIssuedAgainstMe, '/complaint/get/<string:email>')
api.add_resource(BatchAllotment, '/batch_allotment/<string:address>/<string:shopType>/<string:date>')
api.add_resource(ShopsOfSameBatch, '/same_batch/<string:email>')
api.add_resource(BatchAllotmentDetails, '/batch/<string:tense>/<string:email>')
api.add_resource(ShopDetails, '/shop/details/<string:email>')
api.add_resource(About, '/about')

if __name__ == '__main__':
    atStarting()
    app.run(debug=True)
