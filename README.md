# Prometheus

> ## ⚠️ Important Notice
> This project is currently not in a production state and is under active development. Updates and fixes are being implemented to bring the app to a production-ready state. Please check back for updates or contribute to its progress.

In ancient Greek mythology, Prometheus was a Titan revered for his cunning and foresight. Defying the Olympian gods, he bestowed upon humanity a gift of immeasurable value – fire. This was not just literal fire, but a symbol of technology, knowledge, and the spark of civilization itself. Prometheus, whose name means 'forethought', was celebrated as a champion of mankind, empowering them with the tools for progress and enlightenment, much to the chagrin of Zeus and the other gods who wished to keep humans in a state of dependency and ignorance.

## Enlightenment Through Education

Mirroring this legendary benefactor, the Prometheus app emerges as a beacon of hope and empowerment within the confinements of prison walls. It offers inmates a transformative tool – a comprehensive platform providing access to educational resources, degree plans, course schedules, and more. By equipping inmates with technology and knowledge, Prometheus paves a path for their reentry into society. Like the mythical fire, it ignites a new beginning, fostering personal growth, intellectual development, and the promise of a brighter, reformed future. This digital mentor opens doors to a world beyond bars, offering a chance for redemption and the rebuilding of lives through the power of education.

---

## Getting Started: Setup & Deployment

These instructions will help you set up the basic environment using Docker Compose. For advanced SSL/TLS and Kerberos configuration (including certificate and key generation, CSR submission, PEM conversion, and keytab creation), please see the [Advanced Configuration: SSL/TLS and Kerberos Setup](#advanced-configuration-ssltls-and-kerberos-setup) section below.

### Prerequisites

- **Windows AD DS Server:** Ensure you have a Windows Active Directory Domain Services (AD DS) server available.
- **Service Account:** A dedicated service account is required.
- **Docker Desktop (or equivalent):** Install Docker Desktop (or your preferred Docker environment).
- **DNS Configuration:** Set up proper forward and reverse lookups for your server/workstation.

### Basic Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/brandonhenness/Prometheus.git
   cd Prometheus
   ```

2. **Copy the Environment Template**

   Create a `.env` file from the provided template:

   - **Windows (Command Prompt):**
     ```cmd
     copy .env.template .env
     ```
   - **Mac/Linux (Terminal):**
     ```bash
     cp .env.template .env
     ```

   Then, open the newly created `.env` file and adjust the settings to meet your needs.

3. **Build and Launch the Environment**

   Run the following command to build and start all containers in detached mode:
   ```bash
   docker-compose up -d --build
   ```

4. **Configure Canvas SAML Authentication**

   Once the containers are running, set up Canvas SAML Authentication as required. The Docker Compose build automatically downloads and builds the latest production code for Canvas LMS. Refer to your internal documentation for the SAML settings in Canvas.

---

## Advanced Configuration: SSL/TLS and Kerberos Setup

This section describes how to request and configure your SSL/TLS certificates and generate a Kerberos keytab file. **All generated certificate files (PEM format) and the keytab file should be placed in the `certs` directory.**

### A. Submitting CSRs Using the MMC Certificates Snap‑in

1. **Open MMC and Add the Certificates Snap‑in:**
   - Press **Win+R**, type `mmc`, and press **Enter**.
   - In MMC, go to **File > Add/Remove Snap‑in…**
   - Select **Certificates**, click **Add**, choose **Computer account** (if the certificate is for a server), then **Local computer**, and click **Finish**.
   - Click **OK** to return to MMC.

2. **Request a New Certificate:**
   - In the left pane, expand **Certificates (Local Computer)** → **Personal**.
   - Right-click **Certificates** under **Personal** and choose **All Tasks > Request New Certificate…**
   - Click **Next** on the welcome screen.

3. **Select the Enrollment Policy:**
   - On the **Select Certificate Enrollment Policy** page, ensure **Active Directory Enrollment Policy** is selected.
   - Click **Next**.

4. **Choose a Certificate Template:**
   - On the **Request Certificates** page, select a certificate template that supports custom subject names (for example, a custom template based on the Web Server template).
   - Click the link that says **More information is required to enroll for this certificate. Click here to configure certificate settings.**

5. **Configure Certificate Properties:**
   - **Subject Tab:**  
     - Select **Supply in the request**.
     - Enter the **Common Name (CN)** as:  
       ```
       *.<YOUR_DOMAIN>
       ```
       Replace `<YOUR_DOMAIN>` with your actual domain (e.g., `prometheus.example.com`).
   - **Subject Alternative Name (SAN) Tab:**  
     - Add a **DNS Name**: `*.<YOUR_DOMAIN>`
     - Add another **DNS Name**: `<YOUR_DOMAIN>`
   - Adjust any additional settings (key length, key usage, etc.) as required.
   - Click **OK**.

6. **Enroll and Retrieve the Certificate:**
   - Click **Enroll**.  
     - If manual approval is required, your request will be submitted for approval; otherwise, the certificate is issued immediately.
   - Once issued, the certificate will appear under **Personal > Certificates**.

7. **Export the Certificate (Optional):**
   - To export the certificate (including the private key) as a PFX, right-click the certificate, select **All Tasks > Export…**, and follow the Certificate Export Wizard.
   - Save the PFX file; you will later convert it to PEM format.

### B. Converting PFX Files to PEM Format

After obtaining your certificates as PFX files from the CA, convert them to PEM format using OpenSSL. **Place all resulting PEM files in the `certs` directory.**

#### Canvas Service Provider Certificate and Key

- **Extract the Private Key:**
  ```bash
  openssl pkcs12 -in canvas-sp.pfx -nocerts -nodes -out canvas-sp-key.pem
  ```
- **Extract the Certificate:**
  ```bash
  openssl pkcs12 -in canvas-sp.pfx -nokeys -clcerts -out canvas-sp-cert.pem
  ```

#### Identity Provider (IdP) Certificate and Key

- **Extract the Private Key:**
  ```bash
  openssl pkcs12 -in idp.pfx -nocerts -nodes -out idp-key.pem
  ```
- **Extract the Certificate:**
  ```bash
  openssl pkcs12 -in idp.pfx -nokeys -clcerts -out idp-cert.pem
  ```

#### NGINX Certificate and Key

- **Extract the Private Key:**
  ```bash
  openssl pkcs12 -in nginx.pfx -nocerts -nodes -out nginx-key.pem
  ```
- **Extract the Certificate:**
  ```bash
  openssl pkcs12 -in nginx.pfx -nokeys -clcerts -out nginx-cert.pem
  ```
- **Extract the CA Certificate Chain:**
  (A warning about the `-chain` option being ignored is normal.)
  ```bash
  openssl pkcs12 -in nginx.pfx -cacerts -nokeys -out ca-chain.pem
  ```

### C. Creating a Kerberos Keytab File

A Kerberos keytab file securely stores keys for a service principal, allowing your service to authenticate with Kerberos automatically.

For a service hosted at `<YOUR_DOMAIN>` (e.g., `prometheus.example.com`), you need a keytab for the principal:
```
HTTP/<YOUR_DOMAIN>@<YOUR_REALM>
```
Replace `<YOUR_DOMAIN>` with your domain and `<YOUR_REALM>` with your Kerberos realm.

#### Using Windows ktpass

1. **Prepare Your Service Account and SPN:**
   - Ensure you have a service account (e.g., `svc_prometheus`) and that its SPN is set correctly:
     ```powershell
     setspn -S HTTP/<YOUR_DOMAIN> svc_prometheus
     ```
     If you receive a duplicate SPN error, remove the SPN from the old account using ADSI Edit or `setspn -D`.

2. **Run the ktpass Command:**
   Open an elevated command prompt (as a domain administrator) and run one of the following commands (adjusting the encryption type as needed):

   For AES256 (if supported):
   ```batch
   ktpass /out prometheus.keytab /princ HTTP/<YOUR_DOMAIN>@<YOUR_REALM> /mapuser svc_prometheus@<YOUR_REALM> /pass * /crypto AES256-SHA1 /ptype KRB5_NT_PRINCIPAL /kvno 1
   ```
   Or, if AES256 is not supported, try AES128:
   ```batch
   ktpass /out prometheus.keytab /princ HTTP/<YOUR_DOMAIN>@<YOUR_REALM> /mapuser svc_prometheus@<YOUR_REALM> /pass * /crypto AES128-SHA1 /ptype KRB5_NT_PRINCIPAL /kvno 1
   ```
   You will be prompted for the service account's password. On success, a file named `prometheus.keytab` will be created.

3. **Verify the Keytab File:**
   Use a tool like `klist` to inspect the keytab:
   ```batch
   klist -k -t -K prometheus.keytab
   ```
   This command lists the principals and key versions in the keytab file.

4. **Place the Keytab File:**
   Move or copy `prometheus.keytab` into the **certs** directory (or into the directory specified in your Docker Compose, for example, if you reference it as `krb5.keytab`).

---

## Build and Launch the Environment

After you have prepared all certificates, keys, and the keytab file in the **certs** directory, build and start the Docker containers:

```bash
docker-compose up -d --build
```

---

## Configure Canvas SAML Authentication

Once the containers are running, configure Canvas SAML Authentication as required. The Docker Compose build automatically downloads and builds the latest production code for Canvas LMS. Refer to your internal documentation for the SAML settings in Canvas.

---

## Current Features

- **User Authentication Using Kerberos:** Secure login leveraging the Kerberos protocol.
- **Session Management with Redis:** Efficient session storage and management.
- **SAML SSO Support for Canvas LMS:** Single Sign-On integration for Canvas LMS using Kerberos on a SAML Identity Provider.
- **Latest Production Release of Canvas LMS:** Fully functional and up-to-date production build of Canvas LMS.

*Note: Additional features and integrations are under active development. See the Planned Features section for upcoming enhancements.*

---

## Planned Features

### Comprehensive Educational Resources
- **Access to Learning Material:** Provides inmates with a wide range of educational content, including textbooks, articles, and interactive learning modules.
- **Curated Educational Links:** Links to approved online resources, ensuring safe and relevant educational material is accessible.

### Personalized Learning Experience
- **Custom Degree Plans:** Inmates can explore and customize their degree paths based on personal interests and goals.
- **Course Scheduling:** Automates class roster creation, reducing manual administrative work.

### Academic Management
- **Transcript Services:** Provides easy access to academic transcripts for tracking and sharing progress.
- **Study Time Planner:** Tools to help inmates optimize their study time effectively.

### Computer Lab Scheduling
- **Digital Lab Time Scheduling:** Allows students to schedule computer lab time while automatically avoiding class conflicts.

### Instructor Interaction
- **Office Hours Scheduling:** Facilitates one-on-one interactions by enabling students to sign up for instructor office hours via the website.

### Staff-Specific Features
- **Asset Management:** Enables education staff to manage educational materials using barcodes and signature pads, syncing inventory across prison sites.
  
### Reentry Support
- **Reentry Planning Resources:** Offers guidance on using educational achievements for reintegration into society.
- **Career Pathways:** Connects academic achievements with potential career opportunities post-release.

### Community Engagement
- **News/Blogging Section:** Provides a platform for approved student groups to submit and share news articles.

### User-Centric Design
- **Intuitive Interface:** Designed for ease of use in unique prison environments.
- **Accessibility Features:** Ensures the platform is accessible to all users, including those with disabilities.

### Security and Privacy
- **Secure Access:** Complies with institutional regulations for user data privacy and app security.
- **Content Filtering:** Enforces rigorous content filtering aligned with prison safety standards.
- **Active Directory Integration:** Supports single sign-on via existing user credentials.

### Future Integrations
- **Integration with DOC Systems:** Plans to synchronize with Department of Corrections systems to enhance data sharing and operational efficiency.

Prometheus aims to revolutionize education in correctional facilities by fostering a culture of learning and growth while adhering to institutional policies and ensuring user security.

---

## License

Prometheus is licensed under the [GNU General Public License v3.0](LICENSE).

---

Developed with ❤️ by [Brandon Henness](https://github.com/brandonhenness).