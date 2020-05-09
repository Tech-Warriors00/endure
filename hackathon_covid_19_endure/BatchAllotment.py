# controls batch allotment related all functionality

import mysql.connector
import _thread as thread
import BatchAllotmentEmailNotification as sendNotification
import DatabaseConnection as crud
import Pauls_Algorithm as paul


def sendEmail(allotedTiming, date):
    index = -1
    for x in allotedTiming:
        index += 1
        for y in allotedTiming.get(x):
            inTime = ''
            outTime = ''
            if index == 0:
                inTime = '6:00 AM'
                outTime = '10:00 PM'
            elif index == 1:
                inTime = '10:00 PM'
                outTime = '2:00 PM'
            elif index == 2:
                inTime = '2:00 PM'
                outTime = '6:00 PM'
            else:
                inTime = '6:00 PM'
                outTime = '10:00 PM'

            mailingAddress = y
            name, shopId = crud.getOwnerName(mailingAddress)
            modifiedDate = crud.modifyDate(date)
            sendNotification.sendMail(mailingAddress, modifiedDate, index + 1, inTime, outTime,
                                      name, shopId)
        # y ends
    # x ends
    print('All notifications sent successfully.')


def createView(myDB, address, shopType, date):
    try:
        cursor = myDB.cursor(dictionary=True)

        # get day from SQL
        cursor.execute(
            "SELECT date_format('" + date + "', '%w') `day`;"
        )
        res = cursor.fetchall()

        day = ''
        for c in res:
            x = int(c['day'])
            print(x)
            if x == 1:
                day = 'mon'
            elif x == 2:
                day = 'tue'
            elif x == 3:
                day = 'wed'
            elif x == 4:
                day = 'thu'
            elif x == 5:
                day = 'fri'
            elif x == 6:
                day = 'sat'
            else:
                day = 'sun'
            break

        print('Day:', day)
        # create table
        cursor = myDB.cursor(dictionary=True)
        cursor.execute(
            "CREATE VIEW `batchdatabase`.`batch_allotment` AS "
            "SELECT `shop_id`, `email`, `shop_name`, `batch1`,  `batch2`, `batch3`, `batch4` "
            "FROM `batchdatabase`.`owner` WHERE `address` = '" + address + "' AND `type` = '" + shopType + "' "
            "AND `is_verified` = 1 AND `is_active` = 1 AND `" + day + "` = '1';"
        )

        # fetch data
        cursor.execute(
            "SELECT * FROM `batchdatabase`.`batch_allotment`;"
        )
        res = cursor.fetchall()

        # store in list: [[batch1, batch2, batch3, batch4, email],[...]...]
        list = []
        for x in res:
            list.append([int(x['batch1']), int(x['batch2']), int(x['batch3']), int(x['batch4']), str(x['email'])])
        # x ends

        allotedTiming = paul.sendInput(4, list)     # return type: Dictionary

        print('\n\nAllotment Given:')
        for x in allotedTiming:
            print(allotedTiming.get(x))

        # now, update shop_<id>: delete given day's allotment and set new allotment details.

        # delete old data from `shop_<id>` before inserting new data
        for x in allotedTiming:
            for y in allotedTiming.get(x):
                # get email details from view: `batch_allotment`
                currentEmail = y
                cursor.execute(
                    "SELECT `shop_id` FROM `batchdatabase`.`owner` WHERE `email` = '" + currentEmail + "';"
                )
                res = cursor.fetchall()
                currentShopId = ''
                for z in res:
                    currentShopId = str(z['shop_id'])
                    break

                cursor.execute(
                    "DELETE FROM `batchdatabase`.`shop_" + currentShopId + "` WHERE(`date` = '" + date + "');"
                )
                cursor.execute(
                    "DELETE FROM `batchdatabase`.`batch_junk` WHERE(`date` = '" + date + "' "
                    "AND `shop_id` = '" + currentShopId + "');"
                )

        # Update one table at a time
        for x in allotedTiming:
            inTime = ''
            outTime = ''
            if x == 1:
                inTime = '06:00:00'
                outTime = '10:00:00'
            elif x == 2:
                inTime = '10:00:00'
                outTime = '14:00:00'
            elif x == 3:
                inTime = '14:00:00'
                outTime = '18:00:00'
            else:
                inTime = '18:00:00'
                outTime = '22:00:00'

            for y in allotedTiming.get(x):
                # get email, phone, shopName details from view: `batch_allotment`
                currentEmail = y
                cursor.execute(
                    "SELECT `shop_id`, `phone`, `shop_name` FROM `batchdatabase`.`owner` "
                    "WHERE `email` = '" + currentEmail + "';"
                )
                res = cursor.fetchall()
                currentShopId = ''
                currentPhone = ''
                currentShopName = ''
                for z in res:
                    currentShopId = str(z['shop_id'])
                    currentPhone = str(z['phone'])
                    currentShopName = str(z['shop_name'])
                    break

                # insert new data to `shop_<id>`
                cursor.execute(
                    "INSERT INTO `batchdatabase`.`shop_" + currentShopId + "` (`date`, `incoming_time`, "
                    "`outgoing_time`) VALUES('" + date + "', '" + inTime + "', '" + outTime + "');"
                )
                # insert new data to `batch_junk`
                cursor.execute(
                    "INSERT INTO `batchdatabase`.`batch_junk` (`date`, `address`, `shop_id`, `name`, `type`, "
                    "`email`, `phone`, `incoming_time`, `outgoing_time`) "
                    "VALUES('" + date + "', '" + address + "', '" + currentShopId + "', '" + currentShopName + "', "
                    "'" + shopType + "', '" + currentEmail + "', '" + currentPhone + "', "
                    "'" + inTime + "', '" + outTime + "');"
                )

        # send emails using multi-threading
        try:
            thread.start_new_thread(sendEmail, (allotedTiming, date))
        except BaseException as error:
            print('Multi-threading error:')
            print(error)

        # finally, drop View
        cursor = myDB.cursor()
        cursor.execute(
           "DROP VIEW `batchdatabase`.`batch_allotment`;"
        )
        return True
    except mysql.connector.Error as err:
        print('MySQL Error:')
        print(err)
        # finally, drop View
        cursor = myDB.cursor()
        cursor.execute(
            "DROP VIEW `batchdatabase`.`batch_allotment`;"
        )
        return False
    except BaseException as error:
        print('Error:')
        print(error)
        # finally, drop View
        cursor = myDB.cursor()
        cursor.execute(
            "DROP VIEW `batchdatabase`.`batch_allotment`;"
        )
        return False
