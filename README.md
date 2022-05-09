# 🏔️ RATEOTU Server

## 📝 Overview

![auth-registration](https://user-images.githubusercontent.com/25624642/166401575-8c132560-3939-40d4-998d-17d14aff009a.gif)
![acc-activation](https://user-images.githubusercontent.com/25624642/166405618-c2606276-1e7e-4ee2-8c50-1a765827b728.gif)

![client-app-1](https://user-images.githubusercontent.com/25624642/166405584-207802bc-45dc-4f85-9743-9b8524de63c8.gif)
![client-app-2](https://user-images.githubusercontent.com/25624642/166405611-ae4f9d17-d6e3-4db4-9511-450cf6d17190.gif)

![client-staff-app-1](https://user-images.githubusercontent.com/25624642/166406192-06189a41-9a0e-4590-a125-651682389418.gif)
![client-staff-app-2](https://user-images.githubusercontent.com/25624642/166406308-85650cdc-454d-4e57-998a-510f362df764.gif)
![client-staff-app-3](https://user-images.githubusercontent.com/25624642/166407361-0a7b5957-8896-4a26-b36e-197f52ce3729.gif)

![employee-logout](https://user-images.githubusercontent.com/25624642/166407612-06716519-7c04-4e75-9009-f0b1bc609b66.gif)

## 🏁 Requirements

Make sure you have [Docker](https://docs.docker.com/get-docker/) installed on your computer.

## 🚀 Usage

Just run the following command at the root of app project (directory where `compose-local.yml` is located):

```bash
docker-compose -f compose-local.yml up --build
```

This will start all dependent services inside Docker containers. Once they're up and running, you can visit [http://127.0.0.1:3000/](http://127.0.0.1:3000/) to view the customer web app in the browser or [http://127.0.0.1:3005/](http://127.0.0.1:3005/) to view the employee web app.

**To load initial fixtures use:**

```bash
docker-compose -f compose-local.yml run --rm django python manage.py loaddata db_dump.json
```

## 📰 Project Docs

You can read the project documentation at [http://127.0.0.1:4000/](http://127.0.0.1:4000/).

## ☑️ Todo List

- [ ] Add Facebook like notifications, with a dropdown and list/feed view (to have a permament historical record of each notification)
- [ ] Add Table order tracking

*NOTE:*
This web app was developed in Windows 10 using Docker + WSL2.

## ©️ License

This project is [MIT](https://opensource.org/licenses/MIT) licensed.
