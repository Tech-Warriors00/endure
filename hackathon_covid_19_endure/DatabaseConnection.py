# this class checks if tables are created or not, if not then this class creates the tables.

import mysql.connector
import time
import _thread as thread
import CRUDOperatations as crud
import BatchAllotment as allot

# import Search
# import SendNotificationEmail


def getConnection():
    myDB = mysql.connector.connect(user="codebuddy", password="", host="127.0.0.1", port=3307)
    # use 3306 for other (your) system(s), no password
    if myDB is not None:
        return myDB
    else:
        return False


def checkExistenceOfDatabase(myCursor):
    try:
        myCursor.execute("CREATE DATABASE batchdatabase")
    except:
        pass


def checkExistenceOfTables(myCursor):
    print('checkForTables()')
    try:  # shopkeeper's table
        print('checking shopkeeper table...')
        myCursor.execute(
            "CREATE TABLE `batchdatabase`.`owner`( `shop_id` INT NOT NULL AUTO_INCREMENT, `name` VARCHAR(100) "
            "NOT NULL, `type` VARCHAR(100) NULL, `shop_name` VARCHAR(100) NULL, `address` VARCHAR(300) NULL, `phone` "
            "VARCHAR(15) NOT NULL, `email` VARCHAR(100) NOT NULL, `password` VARCHAR(100) NULL, "
            "`otp` VARCHAR(100) NULL, `is_verified` VARCHAR(100) NOT NULL DEFAULT 0, `is_active` VARCHAR(100) "
            "NOT NULL DEFAULT 0, `mon` CHAR(1) NOT NULL DEFAULT '1', `tue` CHAR(1) NOT NULL DEFAULT '1', "
            "`wed` CHAR(1) NOT NULL DEFAULT '1', `thu` CHAR(1) NOT NULL DEFAULT '1', `fri` CHAR(1) NOT NULL "
            " DEFAULT '1', `sat` CHAR(1) NOT NULL DEFAULT '1', `sun` CHAR(1) NOT NULL DEFAULT '1', "
            " `batch1` CHAR(1) NOT NULL, `batch2` CHAR(1) NOT NULL, `batch3` CHAR(1) NOT "
            "NULL, `batch4` CHAR(1) NOT NULL, PRIMARY KEY(`shop_id`), UNIQUE INDEX `phone_UNIQUE`(`phone` ASC) "
            " VISIBLE, UNIQUE INDEX `email_UNIQUE`(`email` ASC) VISIBLE);"
        )
        print("'shopkeeper table created...")

        # setting start value for shop_id
        myCursor.execute(
            "ALTER TABLE `batchdatabase`.`owner` AUTO_INCREMENT = 100000;"
        )
        print('shopkeeper creation completed')
    except BaseException as err:
        print(err)
    try:  # viewer's table
        print('checking viewer table...')
        myCursor.execute(
            "CREATE TABLE `batchdatabase`.`user`( `name` VARCHAR(100) NOT NULL, "
            "`address` VARCHAR(300) NULL, `phone` VARCHAR(15) NULL, `email` VARCHAR(100) NOT NULL, "
            "`otp` VARCHAR(100) NULL, `password` VARCHAR(100) NULL, `is_verified` CHAR(1) NOT NULL DEFAULT 0, "
            "`is_active` CHAR(1) NOT NULL DEFAULT 0, PRIMARY KEY(`email`), UNIQUE INDEX `phone_UNIQUE`(`phone` "
            "ASC) VISIBLE);"
        )
        print('viewer table created')
    except BaseException as err:
        print(err)
    try: # complaint table
        print('checking complaint table...')
        myCursor.execute(
            "CREATE TABLE `batchdatabase`.`complaint`(`date` DATE, "
            "`time` TIME, `issued_by` VARCHAR(100), `issued_to` VARCHAR(100), "
            "`reason` VARCHAR(300) NULL DEFAULT 'None', PRIMARY KEY(`date`, `time`, `issued_by`, `issued_to`));"
        )
        print('complaint creation completed')
    except BaseException as err:
        print(err)
    try: # batch_junk table
        print('checking batch_junk table...')
        myCursor.execute(
            "CREATE TABLE `batchdatabase`.`batch_junk`( "
            "`date` DATE, `address` VARCHAR(300), `shop_id` INT, `name` VARCHAR(100), `type` "
            "VARCHAR(100), `email` VARCHAR(100), `phone` VARCHAR(100), `incoming_time` TIME, " 
            "`outgoing_time` TIME, PRIMARY KEY(`date`, `email`, `type`, `incoming_time`, `outgoing_time`)); "
        )
        print('batch_junk creation completed')
    except BaseException as err:
        print(err)


def start():
    myDB = getConnection()

    if myDB is not None:
        myCursor = myDB.cursor()
        print('start()')
        print(myDB)
        checkExistenceOfDatabase(myCursor)
        checkExistenceOfTables(myCursor)
        myDB.commit()
    else:
        print('Database not connected.')


def login(of, email, password):
    myDB = getConnection()
    myCursor = myDB.cursor()

    # step 1: find account
    myCursor.execute("SELECT * FROM `batchdatabase`.`" + of + "` WHERE email = '" + email + "';")
    userAccount = myCursor.fetchall()
    i = 0
    for x in userAccount:
        i += 1

    if i > 0:  # account found
        print('account found')
        # step 2: check account is verified or not
        cursor = myDB.cursor(dictionary=True)
        cursor.execute("SELECT is_verified FROM `batchdatabase`.`" + of + "` WHERE email = '" + email + "';")
        validationInfo = cursor.fetchall()

        j = 0
        for x in validationInfo:
            print(x)
            print(x['is_verified'])
            if x['is_verified'] == '1':
                j += 1

        if j > 0:  # account is valid
            print('account is valid')
            # step 3: match password
            cursor.execute("SELECT password from `batchdatabase`.`" + of + "` WHERE email = '" + email + "';")
            isCorrect = False
            passwordInfo = cursor.fetchall()
            for x in passwordInfo:
                if x['password'] == password:
                    isCorrect = True

            if isCorrect is True:  # password matched! account is verified.
                print('password matched')

                # now, update `is_account_active` = 1
                cursor.execute(
                    "UPDATE `batchdatabase`.`" + of + "` SET `is_active` = '1' WHERE(`email` = '" + email + "');"
                )
                myDB.commit()
                return True
            else:
                return 'Wrong password entered.'
        else:  # account is invalid
            return 'Account is not verified.'
    else:  # account not found
        return 'No such account exists.'


# send customer's list to owner
def getCustomersInLocality(address):
    try:
        myDB = getConnection()
        cursor = myDB.cursor(dictionary=True)
        cursor.execute(
            "SELECT `name` FROM `batchdatabase`.`user` WHERE `address` = '" + address + "';"
        )
        res = cursor.fetchall()
        print(res)
        return res
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False


# send shop details of shops present in same locality and of the same category
def getShopsInLocalityOfSameOrNotCategory(shopType, address):
    """
    :param shopType: 'None': display all shops; else display shops according to same category
    """
    try:
        myDB = getConnection()
        cursor = myDB.cursor(dictionary=True)

        if shopType is not None:
            cursor.execute(
                "SELECT `shop_id`, `name`, `shop_name`, `phone`, `email`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, "
                "`sun` FROM `batchdatabase`.`owner` WHERE `address` = '" + address + "' AND `type` = '" +
                shopType + "';"
            )
        else:
            cursor.execute(
                "SELECT `shop_id`, `name`, `shop_name`, `phone`, `email`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, "
                "`sun` FROM `batchdatabase`.`owner` WHERE `address` = '" + address + "';"
            )

        res = cursor.fetchall()
        print(res)
        return res
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False


# via DatabaseConnection to other class
def insertIntoUser(name, address, phone, email, password):
    myDB = getConnection()
    return crud.insertIntoUser(myDB, name, address, phone, email, password)


def insertIntoOwner(name, shop_type, shop_name, address, phone, email, password, mon, tue, wed, thu, fri, sat,
                    sun, b1, b2, b3, b4):
    myDB = getConnection()
    return crud.insertIntoOwner(myDB, name, shop_type, shop_name, address, phone, email, password, mon, tue, wed,
                                thu, fri, sat, sun, b1, b2, b3, b4)


def modifyDate(date):
    try:
        myDB = getConnection()
        cursor = myDB.cursor(dictionary=True)
        cursor.execute(
            "SELECT date_format('" + date + "', '%W %d, %M %y') `date`;"
        )
        res = cursor.fetchall()
        modifiedDate = ''
        for x in res:
            modifiedDate = x['date']
            break

        return modifiedDate
    except mysql.connector.Error as err:
        print("MySQL Error:")
        print(err)
        return False
    except BaseException as error:
        print("Error:" + str(error))
        return False


# function to verify otp and set `is_verified` = 1 and `is_active` = 1
def verifyCode(of, email, otp):
    myDB = getConnection()
    return crud.verifyCode(myDB, of, email, otp)


def updateUser(email, name, address, phone):
    myDB = getConnection()
    return crud.updateUser(myDB, email, name, address, phone)


def updateOwner(email, name, shop_type, shop_name, address, phone, mon, tue, wed, thu, fri, sat, sun,
                b1, b2, b3, b4):
    myDB = getConnection()
    return crud.updateOwner(myDB, email, name, shop_type, shop_name, address, phone, mon, tue, wed, thu, fri,
                            sat, sun, b1, b2, b3, b4)


def deactivateAccount(of, email):
    myDB = getConnection()
    return crud.deactivateAccount(myDB, of, email)


def issueComplaint(issuedBy, issuedTo, reason):
    myDB = getConnection()
    return crud.issueComplaint(myDB, issuedBy, issuedTo, reason)


def getComplaintIssuedAgainstMe(email):
    myDB = getConnection()
    return crud.getComplaintIssuedAgainstMe(myDB, email)


def batchAllotment(address, shopType, date):
    myDB = getConnection()
    return allot.createView(myDB, address, shopType, date)


# get all shops that belong to my batch CURDATE()
def getShopsOfSameBatch(email):
    myDB = getConnection()
    return crud.getShopsOfSameBatch(myDB, email)


def getBatchAllotmentDetails(email, tense):
    """
    :param tense: 'past', 'present' or 'future'
    """
    myDB = getConnection()
    return crud.getBatchAllotmentDetails(myDB, email, tense)


def getOwnerName(email):
    myDB = getConnection()
    return crud.getOwnerName(myDB, email)


def getShopDetails(email):
    myDB = getConnection()
    return crud.getShopDetails(myDB, email)


#batchAllotment("jj rd, ranchi, jharkhand, 834001 upper bazar", 'cafe', '2020-05-07')