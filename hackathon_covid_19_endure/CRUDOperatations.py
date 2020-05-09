# this class handles all database related operations

import mysql.connector
import UserOwnerVerificationCodeViaEmail as sendVerification


def insertIntoUser(myDB, name, address, phone, email, password):
    print('inserting user data in `user`...')
    myDB.autocommit = False
    cursor = myDB.cursor(dictionary=True)
    try:
        # step 1: insert data in database
        cursor.execute(
            "INSERT INTO `batchdatabase`. `user`(`name`, `address`, `phone`, `email`, `password`) "
            "VALUES('" + name + "', '" + address + "', '" + phone + "', '" + email + "', '" + password + "');"
        )
        print('inserted successfully')

        # step 2: generate verification code and send email
        print('sending mail...')
        isSent = sendVerification.sendMail(myDB, cursor, 'user', email)

        # step 4: if email successfully sent then myDB.commit()
        if isSent is True:
            myDB.autocommit = True
            myDB.commit()
            return 'Verification code has been sent to your email address. Check your email and enter the code.'
        else:
            myDB.rollback()
            myDB.autocommit = True
            return 'Cannot send verification email. Please try again after some time.'

    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        myDB.rollback()
    except BaseException as error:
        print("Error:" + str(error))
        myDB.rollback()
    finally:
        myDB.autocommit = True
    return False


def insertIntoOwner(myDB, name, shop_type, shop_name, address, phone, email, password, mon, tue, wed, thu, fri, sat,
                    sun, b1, b2, b3, b4):
    print('inserting owner data in `owner`...')
    myDB.autocommit = False
    cursor = myDB.cursor(dictionary=True)
    try:
        # step 1: insert data in database
        cursor.execute(
            "INSERT INTO `batchdatabase`.`owner`(`name`, `type`, `shop_name`, `address`, `phone`, `email`, " 
            "`password`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`, `batch1`, `batch2`, `batch3`, `batch4`) "
            "VALUES('" + name + "', '" + shop_type + "', '" + shop_name + "', '" + address + "', '" + phone + "', "
            "'" + email + "', '" + password + "', " 
            "'" + mon + "', '" + tue + "', '" + wed + "', '" + thu + "', '" + fri + "', '" + sat + "', '" + sun + "', "
            "'" + b1 + "', '" + b2 + "', '" + b3 + "', '" + b4 + "');"
        )
        print('inserted successfully')

        # step 2: create table shop_<shopId>
        cursorX = myDB.cursor(dictionary=True)
        cursorX.execute(
            "SELECT `shop_id` from `batchdatabase`.`owner` WHERE `email` = '" + email + "';"
        )
        info = cursorX.fetchall()

        id = ''
        for x in info:
            print('>>>', x)
            id = str(x['shop_id'])
            break

        print('ID:', id)

        cursor.execute(
            "CREATE TABLE `batchdatabase`. `shop_" + id + "`(`date` DATE NOT NULL,  `incoming_time` "
            "TIME NOT NULL, `outgoing_time` TIME NOT NULL); "
        )

        # step 3: generate verification code and send email
        print('sending mail...')
        isSent = sendVerification.sendMail(myDB, cursor, 'owner', email)

        # step 4: if email successfully sent then myDB.commit()
        if isSent is True:
            myDB.autocommit = True
            myDB.commit()
            return 'Verification code has been sent to your email address. Check your email and enter the code.'
        else:
            myDB.rollback()
            myDB.autocommit = True
            return 'Cannot send verification email. Please try again after some time.'

    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        myDB.rollback()
    except BaseException as error:
        print("Error:" + str(error))
        myDB.rollback()
    finally:
        myDB.autocommit = True
    return False


# deactivate owner/user account
def deactivateAccount(myDB, of, email):
    """
    :param of: 'user' or 'owner'
    """

    cursor = myDB.cursor()
    try:
        cursor.execute(
            "UPDATE `batchdatabase`.`" + of + "` SET `is_active` = '0' WHERE(`email` = '" + email + "');"
        )
        myDB.commit()
        return True
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False


# function to set `is_account_active` = 1 and `is_verified` = 1 once the OTP is sent
def verifyCode(myDB, of, email, otp):
    """
    :param of: 'user' or 'owner'
    """

    cursor = myDB.cursor(dictionary=True)
    cursor.execute("SELECT otp FROM `batchdatabase`.`" + of + "` WHERE email = '" + email + "';")
    otpInfo = cursor.fetchall()
    i = 0

    for x in otpInfo:
        if x['otp'] == otp:
            i += 1
            break
    if i == 1:
        # otp found correct! update DB and set 'is_verified'/'is_active' = 1 (0: not verified)
        try:
            cursor.execute(
                "UPDATE `batchdatabase`.`" + of + "` SET `is_verified` = '1', `is_active` = 1 "
                "WHERE(`email` = '" + email + "');")
            myDB.commit()
            return True
        except:
            return False
    else:
        return False


# update user's data
def updateUser(myDB, email, name, address, phone):
    cursor = myDB.cursor()
    myDB.autocommit = False
    try:
        cursor.execute(
            "UPDATE `batchdatabase`.`user` SET `name` = '" + name + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`user` SET `address` = '" + address + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`user` SET `phone` = '" + phone + "' WHERE(`email` = '" + email + "');"
        )
        myDB.commit()
        myDB.autocommit = True
        return True
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        myDB.rollback()
    except BaseException as error:
        print("Error:" + str(error))
        myDB.rollback()
    finally:
        myDB.autocommit = True
    return False


def updateOwner(myDB, email, name, shop_type, shop_name, address, phone, mon, tue, wed, thu, fri, sat, sun,
                b1, b2, b3, b4):
    cursor = myDB.cursor()
    myDB.autocommit = False
    try:
        print('updating...')
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `name` = '" + name + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `type` = '" + shop_type + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `shop_name` = '" + shop_name + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `address` = '" + address + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `phone` = '" + phone + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `mon` = '" + mon + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `tue` = '" + tue + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `wed` = '" + wed + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `thu` = '" + thu + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `fri` = '" + fri + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `sat` = '" + sat + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `sun` = '" + sun + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `batch1` = '" + b1 + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `batch2` = '" + b2 + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `batch3` = '" + b3 + "' WHERE(`email` = '" + email + "');"
        )
        cursor.execute(
            "UPDATE `batchdatabase`.`owner` SET `batch4` = '" + b4 + "' WHERE(`email` = '" + email + "');"
        )

        myDB.commit()
        myDB.autocommit = True
        print('updated.')
        return True
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        myDB.rollback()
    except BaseException as error:
        print("Error:" + str(error))
        myDB.rollback()
    finally:
        myDB.autocommit = True
    return False


def issueComplaint(myDB, issuedBy, issuedTo, reason):
    try:
        cursor = myDB.cursor(dictionary=True)

        # step 1: get current date
        cursor.execute(
            "SELECT CURDATE() `date`;"
        )
        res = cursor.fetchall()

        date = ''
        for x in res:
            date = str(x['date'])
            break

        print('Date:', date)

        # step 2: get current time
        cursor.execute(
            "SELECT CURTIME() `time`;"
        )
        res = cursor.fetchall()

        time = ''
        for x in res:
            time = str(x['time'])
            break

        print('Time:', time)

        # step 3: insert data in `complaint`
        cursor.execute(
            "INSERT INTO `batchdatabase`.`complaint`(`date`, `time`, `issued_by`, `issued_to`, `reason`) "
            "VALUES('" + date + "', '" + time + "', '" + issuedBy + "', '" + issuedTo + "', '" + reason + "');"
        )
        myDB.commit()
        return True
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False


# get owner's complaints
def getComplaintIssuedAgainstMe(myDB, email):
    try:
        cursor = myDB.cursor(dictionary=True)
        cursor.execute(
            "SELECT date_format(`date`, '%W %d, %M %y') `date`,"
            "TIME_FORMAT(`time`, '%h:%i:00 %p') `time`,"
            "`reason` FROM `batchdatabase`.`complaint` WHERE `issued_to` = '" + email + "';"
        )
        res = cursor.fetchall()
        myComplaints = []

        for x in res:
            myComplaints.append(x)

        print("My Complaints:", myComplaints)
        return myComplaints
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False


# get all shops that belong to my batch CURDATE()
def getShopsOfSameBatch(myDB, email):
    try:
        cursor = myDB.cursor(dictionary=True)
        # get shop_type, address and shop_id
        cursor.execute(
            "SELECT `type`, `address`, `shop_id` FROM `batchdatabase`.`owner` WHERE `email` = '" + email + "';"
        )
        res = cursor.fetchall()
        shopType = ''
        address = ''
        shopId = ''

        for x in res:
            shopType = x['type']
            address = x['address']
            shopId = str(x['shop_id'])
            break

        # get opening_time and closing_time
        cursor.execute(
            "SELECT `incoming_time`, `outgoing_time` FROM `batchdatabase`.`shop_" + shopId + "` WHERE "
            "`date` = CURDATE() AND `incoming_time` <= CURTIME() AND `outgoing_time` >= CURTIME();"
        )
        incomingTime = ''
        outgoingTime = ''
        res = cursor.fetchall()

        for x in res:
            incomingTime = str(x['incoming_time'])
            outgoingTime = str(x['outgoing_time'])
            break
        print('1')
        print('incoming_time:', incomingTime)
        print('outgoing_time:', outgoingTime)
        # fetch all shops that belong to my batch
        cursor.execute(
            "SELECT `shop_id`, `name`, `email`, `phone` FROM `batchdatabase`.`batch_junk` "
            "WHERE `type` = '" + shopType + "' AND `date` = CURDATE() AND `address` = '" + address + "' AND "
            "`incoming_time` = '" + incomingTime + "' AND `outgoing_time` = '" + outgoingTime + "' "
            "AND `email` != '" + email + "';"
        )
        print('2')
        res = cursor.fetchall()

        list = []
        for x in res:
            list.append(x)

        return list
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False


def getBatchAllotmentDetails(myDB, email, tense):
    """
    :param tense: 'past', 'present' or 'future'
    """
    sign = ''
    if tense == 'past':
        sign = '<'
    elif tense == 'present':
        sign = '='
    else:
        sign = '>'

    try:
        cursor = myDB.cursor(dictionary=True)

        # get shopId
        shopId = ''
        cursor.execute(
            "SELECT `shop_id` FROM `batchdatabase`.`owner` WHERE `email` = '" + email + "';"
        )
        res = cursor.fetchall()
        for x in res:
            shopId = str(x['shop_id'])
            break

        cursor.execute(
            "SELECT date_format(`date`, '%W %d, %M %y') `date`, "
            "TIME_FORMAT(`incoming_time`, '%h:%i:00 %p') `incoming_time`, "
            "TIME_FORMAT(`outgoing_time`, '%h:%i:00 %p') `outgoing_time` "
            "FROM `batchdatabase`.`shop_" + shopId + "` "
            "WHERE `date` " + sign + " CURDATE();"
        )
        res = cursor.fetchall()
        list = []

        for x in res:
            list.append(x)

        return list
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False


def getOwnerName(myDB, email):
    try:
        cursor = myDB.cursor(dictionary=True)
        cursor.execute(
            "SELECT `name`, `shop_id` FROM `batchdatabase`.`owner` WHERE `email` = '" + email + "';"
        )
        res = cursor.fetchall()
        name = ''
        shopId = ''

        for x in res:
            name = (str(x['name'])).title()
            shopId = str(x['shop_id'])
            break

        return name, shopId

    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False


def getShopDetails(myDB, email):
    try:
        cursor = myDB.cursor()
        cursor.execute(
            "SELECT `shop_id`, `name`, `shop_name`, `type`, `address`, `phone`, "
            "`mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`, `batch1`, `batch2`, `batch3`, `batch4` "
            "FROM `batchdatabase`.`owner` "
            "WHERE `email` = '" + email + "';"
        )
        row_headers = [x[0] for x in cursor.description]  # this will extract row headers

        res = cursor.fetchall()

        for i in res:
            # converting to JSON format
            return dict(zip(row_headers, i))
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False