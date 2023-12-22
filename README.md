# API Documentation

## Base URL

- **Base URL:** `http://127.0.0.1:8000`

## Authentication

- The API uses token-based authentication.
- Include the `Authorization` header in each request with the format: `Authorization: Token YOUR_TOKEN`.
- `YOUR_TOKEN` can be generated from login or register endpoints

---

## Endpoints of Auth

### 1. **POST /api/register**

#### Description

Used to register the user

#### Request

- **Method:** `POST`
- **URL:** `/api/register`
- **Headers:**
  - `Accept : application/json`
- **Body:**
  ```json
  {
    "username": "Avi",
    "password": "avi123"
  }
  ```

#### Success Response

- **Status Code:** `202 ACCEPTED`
- **Body:**
  ```json
  {
    "token": "7ad992534d8cfbac067e009d6f9538a51b25f5b1",
    "user": {
      "id": 2,
      "username": "Avi",
      "password": "avi123",
      "email": ""
    }
  }
  ```

### 2. **POST /api/login**

#### Description

Registered user can login and receive the token

#### Request

- **Method:** `POST`
- **URL:** `/api/login`
- **Headers:**
  - `Accept : application/json`
- **Body:**
  ```json
  {
    "username": "Ashok",
    "password": "ashok123"
  }
  ```

#### Success Response

- **Status Code:** `202 ACCEPTED`
- **Body:**
  ```json
  {
    "token": "335c24166c158e7cab942082e284662864ea83f2",
    "user": {
      "id": 1,
      "username": "Ashok",
      "password": "pbkdf2_sha256$720000$GbVPvOg7ptRHp0O5YwyAHO$5IDp/Zzzr7XwP2qrI8bGnM1TUeUa/AaQH8hcvGTssoQ=",
      "email": ""
    }
  }
  ```

### 3. **GET /api/logout**

#### Description

User can be logout , the generated token will be removed and become invalid

#### Request

- **Method:** `GET`
- **URL:** `/api/logout`
- **Headers:**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`

#### Success Response

- **Status Code:** `200 OK`

---

## Endpoints of vendor

### 1. **GET /api/vendors**

#### Description

Returns all the basic information of vendor.

#### Request

- **Method:** `GET`
- **URL:** `/api/vendors`
- **Headers:**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  [
    {
      "id": 1,
      "name": "Nvidia",
      "vendor_code": "Bte"
    },
    {
      "id": 2,
      "name": "AMD",
      "vendor_code": "Zjj"
    },
    {
      "id": 3,
      "name": "Intel",
      "vendor_code": "EUp"
    }
  ]
  ```

### 2. **GET /api/vendors/1**

#### Description

Returns the detailed in of specified vendor in url.

#### Request

- **Method:** `GET`
- **URL:** `/api/vendors/<int:vendor_id>`
- **Headers:**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  {
    "id": 1,
    "name": "Nvidia",
    "contact_details": "408-486-2000",
    "address": "Santa Clara, 2788 San Tomas Expy, United States",
    "vendor_code": "Bte"
  }
  ```

### 3. **POST /api/vendors**

#### Description

Add new Vendor in the database

#### Request

- **Method :** `POST`
- **URL :** `/api/vendors`
- **Headers :**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`
- **Body :**
  ```json
  {
    "name": "Intel",
    "contact_details": "800-440-2319",
    "address": "Santa Clara, 2200 Mission College Blvd, United States"
  }
  ```

#### Success Response

- **Status Code:** `201 CREATED`
- **Body:**

  ```json
  {
    "id": 5,
    "name": "Intel",
    "contact_details": "800-440-2319",
    "address": "Santa Clara, 2200 Mission College Blvd, United States",
    "vendor_code": "sXo"
  }
  ```

### 4. **PUT /api/vendors/5**

#### Description

Update Vendor Information, user can updated any field which was added in POST request.

#### Request

- **Method :** `PUT`
- **URL :** `/api/vendors/<int:vendor_id>`
- **Headers :**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`
- **Body :**
  ```json
  {
    "name": "Intel new"
  }
  ```

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  {
    "id": 5,
    "name": "Intel new",
    "contact_details": "800-440-2319",
    "address": "Santa Clara, 2200 Mission College Blvd, United States",
    "vendor_code": "sXo"
  }
  ```

### 5. **DELETE /api/vendors/5**

#### Description

Delete the Vendor with given id in URL.

#### Request

- **Method :** `DELETE`
- **URL :** `/api/vendors/<int:vendor_id>`
- **Headers :**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  { "res": "Object deleted!" }
  ```

---

## Endpoints of Purchase orders

### 1. **GET api/purchase_orders**

#### Description

Returns all the purchase order with infomation about vendor id, order_date, items list and status (default status is pending).

#### Request

- **Method:** `GET`
- **URL:** `/api/purchase_orders`
- **Headers:**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  [
    {
      "id": 1,
      "po_number": "NPu",
      "vendor": 1,
      "order_date": "2023-12-19T17:31:37.935510Z",
      "items": [
        {
          "name": "RTX 3070",
          "Type": "GPU",
          "Price": "37000"
        },
        {
          "name": "RTX 2070 super",
          "Type": "GPU",
          "Price": "27000"
        },
        {
          "name": "RTX 1070 super",
          "Type": "GPU",
          "Price": "12000"
        }
      ],
      "status": "completed"
    },
    {
      "id": 2,
      "po_number": "Wjn",
      "vendor": 1,
      "order_date": "2023-12-19T17:32:33.769360Z",
      "items": [
        {
          "name": "RTX 4070",
          "Type": "GPU",
          "Price": "46000"
        },
        {
          "name": "RTX 2080 TI",
          "Type": "GPU",
          "Price": "38000"
        }
      ],
      "status": "completed"
    }
  ]
  ```

### 2. **GET /api/purchase_orders/1**

#### Description

Returns the detailed of specified purchase order in url.

#### Request

- **Method:** `GET`
- **URL:** `/api/purchase_orders/<int:vendor_id>`
- **Headers:**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  {
    "id": 1,
    "po_number": "NPu",
    "order_date": "2023-12-19T17:31:37.935510Z",
    "delivery_date": "2023-12-20T09:30:00Z",
    "items": [
      {
        "name": "RTX 3070",
        "Type": "GPU",
        "Price": "37000"
      },
      {
        "name": "RTX 2070 super",
        "Type": "GPU",
        "Price": "27000"
      },
      {
        "name": "RTX 1070 super",
        "Type": "GPU",
        "Price": "12000"
      }
    ],
    "quantity": 3,
    "status": "completed",
    "quality_rating": 0.0,
    "issue_date": "2023-12-19T17:31:37.935531Z",
    "acknowledgment_date": "2023-12-20T15:27:05.198965Z",
    "order_completed": "2023-12-22T06:05:17.683106Z",
    "order_cancelled": null,
    "vendor": 1
  }
  ```

### 3. **POST /api/purchase_orders**

#### Description

Add new purchase order in the database

#### Request

- **Method :** `POST`
- **URL :** `/api/purchase_orders`
- **Headers :**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`
- **Body :**
  ```json
  {
    "vendor": 1,
    "delivery_date": "20-12-2023 09:30",
    "items": [
      {
        "name": "RTX 3070",
        "Type": "GPU",
        "Price": "37000"
      },
      {
        "name": "RTX 2070 super",
        "Type": "GPU",
        "Price": "27000"
      }
    ],
    "quality_rating": 0.0
  }
  ```

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  {
    "id": 3,
    "po_number": "NJL",
    "order_date": "2023-12-22T07:08:34.972353Z",
    "delivery_date": "2023-12-20T09:30:00Z",
    "items": [
      {
        "name": "RTX 3070",
        "Type": "GPU",
        "Price": "37000"
      },
      {
        "name": "RTX 2070 super",
        "Type": "GPU",
        "Price": "27000"
      }
    ],
    "quantity": 2,
    "status": "pending",
    "quality_rating": 0.0,
    "issue_date": "2023-12-22T07:08:34.972366Z",
    "acknowledgment_date": null,
    "order_completed": null,
    "order_cancelled": null,
    "vendor": 1
  }
  ```

### 4. **PUT /api/purchase_orders/5**

#### Description

Update purchase order Information, user can updated any field which was added in POST request as well as status field.

Note: If status field is changed to `completed`, will start the calculation for other fields in vendor .i.e `quality_rating_avg` , `on_time_delivery_rate` `fulfillment_rate`

#### Request

- **Method :** `PUT`
- **URL :** `/api/purchase_orders/<int:vendor_id>`
- **Headers :**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`
- **Body :**
  ```json
  "items": [
      {
        "name": "RTX 3070",
        "Type": "GPU",
        "Price": "37000"
      },
      {
        "name": "RTX 2070 super",
        "Type": "GPU",
        "Price": "27000"
      },
      {
        "name": "GTX 1060 TI",
        "Type": "GPU",
        "Price": "12000"
      }
    ],
  ```

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  {
    "id": 3,
    "po_number": "NJL",
    "order_date": "2023-12-22T07:08:34.972353Z",
    "delivery_date": "2023-12-20T09:30:00Z",
    "items": [
      {
        "name": "RTX 3070",
        "Type": "GPU",
        "Price": "37000"
      },
      {
        "name": "RTX 2070 super",
        "Type": "GPU",
        "Price": "27000"
      },
      {
        "name": "GTX 1060 TI",
        "Type": "GPU",
        "Price": "12000"
      }
    ],
    "quantity": 3,
    "status": "pending",
    "quality_rating": 0.0,
    "issue_date": "2023-12-22T07:08:34.972366Z",
    "acknowledgment_date": null,
    "order_completed": null,
    "order_cancelled": null,
    "vendor": 1
  }
  ```

### 5. **DELETE /api/purchase_orders/3**

#### Description

Delete the purchase_orders with given id in URL.

#### Request

- **Method :** `DELETE`
- **URL :** `/api/purchase_orders/<int:vendor_id>`
- **Headers :**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  { "res": "Object deleted!" }
  ```

---

## Endpoints for acknowledgment , performance and Historical performance

### 1. **POST /api/purchase_orders/1/acknowledge**

#### Description

Used by vendors to acknowledge the purchase order.
this endpoint will trigger the calculation of `average_response_time` for vendor and also populated the `acknowledge_date` field

#### Request

- **Method :** `POST`
- **URL :** `/api/purchase_orders/<int:po_id>/acknowledge`
- **Headers :**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`
- **Body :**
  ```json
  {
    "id": 1,
    "po_number": "NPu",
    "order_date": "2023-12-19T17:31:37.935510Z",
    "delivery_date": "2023-12-20T09:30:00Z",
    "items": [
      {
        "name": "RTX 3070",
        "Type": "GPU",
        "Price": "37000"
      },
      {
        "name": "RTX 2070 super",
        "Type": "GPU",
        "Price": "27000"
      },
      {
        "name": "RTX 1070 super",
        "Type": "GPU",
        "Price": "12000"
      }
    ],
    "quantity": 3,
    "status": "completed",
    "quality_rating": 0.0,
    "issue_date": "2023-12-19T17:31:37.935531Z",
    "acknowledgment_date": "2023-12-22T07:40:17.154560Z",
    "order_completed": "2023-12-22T06:05:17.683106Z",
    "order_cancelled": null,
    "vendor": 1
  }
  ```

### 2. **GET /api/vendors/1/performance**

#### Description

Returns performance meterics for Vendors.

#### Request

- **Method:** `GET`
- **URL:** `/api/vendors/<int:vendor_id>/performance`
- **Headers:**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  {
    "id": 1,
    "name": "Nvidia",
    "vendor_code": "Bte",
    "on_time_delivery_rate": 0.0,
    "quality_rating_avg": 0.0,
    "average_response_time": 149999.24465,
    "fulfillment_rate": 100.0
  }
  ```

### 3. **GET /api/vendors/historical**

#### Description

Everytime status is changed to completed in PO a snap of vendor performance metrics is saved in Historical performance DB, can be used for analysis.

#### Request

- **Method:** `GET`
- **URL:** `/api/vendors/historical`
- **Headers:**
  - `Authorization: Token YOUR_TOKEN`
  - `Accept : application/json`

#### Success Response

- **Status Code:** `200 OK`
- **Body:**

  ```json
  [
    {
      "id": 1
      "vendor": 1,
      "date": "2023-12-22T06:03:43.717574Z",
      "on_time_delivery_rate": 0.0,
      "quality_rating_avg": 0.0,
      "average_response_time": 77603.2668525,
      "fulfillment_rate": 100.0
    },
    {
      "id": 2,
      "vendor": 1,
      "date": "2023-12-22T06:05:17.745890Z",
      "on_time_delivery_rate": 0.0,
      "quality_rating_avg": 0.0,
      "average_response_time": 77603.2668525,
      "fulfillment_rate": 100.0
    }
  ]
  ```
