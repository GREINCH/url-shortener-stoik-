# URL Shortener API

## Introduction
The URL Shortener API is a FastAPI application designed to shorten URLs and provide redirection to the original URLs based on unique slugs. This API is ideal for applications that need to condense long URLs into manageable, short links that are easier to share and handle.

## Features
- **Shorten URL**: Converts a long URL into a short URL with an expiration option.
- **Redirect URL**: Redirects to the original long URL based on a unique slug.

## Requirements
- Python 3.10 or higher
- FastAPI
- Uvicorn
- SQLAlchemy

## Local Setup
Follow these steps to set up the project locally:

### 1. Clone the repository:
   ```
   git clone https://github.com/GREINCH/url-shortener-stoik-
   cd url-shortener-stoik-/
   ```


### 2. Create a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies:

```
pip install -r requirements.txt
```

### 4. Run the application:

##### Locally
```
uvicorn api:app --reload  # The `--reload` flag enables hot reloading during development.
The API will be available at http://127.0.0.1:8000.
```

##### Using Docker

To containerize and run the API using Docker, follow these instructions:

Build the Docker image:

```
docker build -t url-shortener .
```

Run the container:

```
docker run -p 80:80 --name url-shortener-instance url-shortener
The API will be accessible at http://127.0.0.1:80.
```
- The API documentation is here:
```
The API will be accessible at http://127.0.0.1:80/docs.
The API will be accessible at http://127.0.0.1:80/redoc.
```

### 5. API Endpoints

##### Shorten URL

- Endpoint: POST /shorten
- Body:
```
{
  "url": "https://youtube.fr",
  "expires_in_days": 10
}
```
- Description: Shortens the provided URL and optionally sets an expiration date.

##### Redirect URL
- Endpoint: GET /{slug}
- Description: Redirects to the original URL associated with the provided slug. For example:
  ```
  http://127.0.0.1:80/A6H432
  ```

### Install a DNS Server

* Following these steps, your domain `url-shortener.local` will resolve to `192.168.1.21` on your local network.
* This allows you to simulate a more realistic production environment without modifying the `/etc/hosts` file on each machine.

##### BIND9 Installation
Execute the following commands to update your system and install BIND9 along with its utilities:

  ```
    sudo apt update && sudo apt upgrade -y
    sudo apt install bind9 bind9-utils bind9-doc dnsutils
  ```

##### Configuration of the DNS Zone
Edit the BIND9 local configuration file:
  ```
    sudo vi /etc/bind/named.conf.local
  ```
Add the following lines to define a new DNS zone for url-shortener.local:
  ```
    zone "url-shortener.local" {
        type master;
        file "/etc/bind/db.url-shortener.local";
    };
  ```

##### Creation of the DNS Zone File
Copy the default zone file to create a new one for url-shortener.local:

  ```
    sudo cp /etc/bind/db.local /etc/bind/db.url-shortener.local
  ```
Edit the new zone file:
  ```
    sudo nano /etc/bind/db.url-shortener.local
  ```
Modify the file to look like this, replacing IP_DU_CLUSTER with 192.168.1.21:
  ```
    ;
    ; BIND data file for local loopback interface
    ;
    $TTL    604800
    @       IN      SOA     url-shortener.local. root.url-shortener.local. (
                                  2024062901     ; Serial
                             604800         ; Refresh
                              86400         ; Retry
                            2419200         ; Expire
                             604800 )       ; Negative Cache TTL
    ;
    @       IN      NS      url-shortener.local.
    @       IN      A       192.168.1.21
  ```

##### Restart BIND9
After modifying the configuration files, restart BIND9 to apply the changes:

  ```
    sudo systemctl restart bind9
  ```

##### Test the Configuration
Use dig or nslookup to test the resolution of your domain:
  ```
    dig url-shortener.local @127.0.0.1
  ```
