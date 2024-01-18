# Сервис по перепродаже билетов на концерты "Спрос на стобоскоп"

***Проект разрабатывается в рамках тренировки***

## Проблема

Чем дальше, тем сложнее строить планы больше, чем на 1-2 недели. Уезжаешь в незапланированную командировку, а билет в театр пропадает. Хочешь устроить внезапное свидание, а соседние места в зале можно купить только через месяц. Можно найти перекупов, но они как минимум возьмут 100% наценку, а как максимум обманут. 

Этот сервис позволит встретиться с человеком, который готов продать билет без большой наценки, быстро и надежно.

## System Design

### Requirements clarifications

#### Functional Requirements

1. Each user has a profile with her full name and a verified phone number. Each person (phone number) should have one unique account.
2. Each user can put up her ticket for sale and mark it as expired. Essential info about the ticket: full name, date, time and place of the event, ticket barcode and price. Also every ticker should be marked with one of the event types. All the tickets should be checked for originality. 
3. Each user has access to feed with available tickets in reverse chronological order.
4. If user wants to buy a ticket, she is redirected to payment page. Money will be sent to an account linked to phone number. After a successful transaction a barcode is shown and the ticket is marked as bought.
5. Unpurchased tickets are marked as expired after the event.

#### Non-Functional Requirements

1. Safety. Both ticket info and client info should have minimal chance of leakage.

### System interface definition

Let's define API methods. All-around list:
* createAccount(user_name, user_login, phone_number)
* getAccountInfo(user_login)
* addTicket(user_id, event_name, event_type, event_timestamp, event_city, ticket_barcode, ticket_price)
* buyTicket(ticket_id)
* getTicketList()
* getTicketListByType(event_type)
* getOutdatedTicketList()
* markTicketAsOutdated(ticket_id)

### Back-of-the-envelope estimation

The system is expected to work over the country. Let's assume we will have 200K overall users with 20K weekly active users. On average a user puts up 5 tickets a week. So to store all the tickets for one day we would need 10Gb of storage.

20000 users * 5 tickets * 100Kb / 7 => 10Gb/day

Thus total space required for 5 years:

10Gb * 365 * 5 ~= 18Tb

### Defining data model

Relational database will be used for data storing.

![Data model](<img/data_model.png>)

### High-level design

***TODO***

### Detailed design

***TODO***

### Identifying and resolving bottlenecks

***TODO***

### Места для доработки

Добавить регистрацию пользователя
Сохранять сессию авторизированного пользователя
Вводить местоположение мероприятия выбором из списка (узнать как это делается - API?)
Хранить штрих-код картинкой (object storage)
Добавить чат для общения между покупателем и продавцом

!! Почитать об устройстве Авито
