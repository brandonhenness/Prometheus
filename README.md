# Prometheus

> ## ⚠️ Important Notice
> This project is currently not in a production state and is under active development. Updates and fixes are being implemented to bring the app to a production ready state. Please check back for updates or contribute to its progress.

In ancient Greek mythology, Prometheus was a Titan revered for his cunning and foresight. Defying the Olympian gods, he bestowed upon humanity a gift of immeasurable value – fire. This was not just literal fire, but a symbol of technology, knowledge, and the spark of civilization itself. Prometheus, whose name means 'forethought', was celebrated as a champion of mankind, empowering them with the tools for progress and enlightenment, much to the chagrin of Zeus and the other gods who wished to keep humans in a state of dependency and ignorance.

## Enlightenment Through Education

Mirroring this legendary benefactor, the Prometheus app emerges as a beacon of hope and empowerment within the confinements of prison walls. It offers inmates a transformative tool – a comprehensive platform providing access to educational resources, degree plans, course schedules, and more. By equipping inmates with technology and knowledge, Prometheus paves a path for their reentry into society. Like the mythical fire, it ignites a new beginning, fostering personal growth, intellectual development, and the promise of a brighter, reformed future. This digital mentor opens doors to a world beyond bars, offering a chance for redemption and the rebuilding of lives through the power of education.

---

## Getting Started: Setup & Deployment

The entire environment is orchestrated using Docker Compose. These instructions apply to both production and development setups.

### Prerequisites

- **Windows AD DS Server:** Ensure you have a Windows Active Directory Domain Services (AD DS) server available.
- **Service Account:** A dedicated service account is required.
- **Docker Desktop (or equivalent):** Install Docker Desktop (or your preferred Docker environment).
- **DNS Configuration:** Set up proper Forward and Reverse lookups for your server/workstation.

### Setup Instructions

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

3. **Prepare Certificates and Keys**

   You must create or obtain the following certificate and key files in the parent directory (relative to the repository root). Ensure these files are available for Docker to mount:

   - **Identity Provider (IdP):**
     - `../idp-cert.pem` → mounted to `/etc/ssl/certs/idp-cert.pem:ro`
     - `../idp-key.pem` → mounted to `/etc/ssl/private/idp-key.pem:ro`
   - **Canvas Service Provider:**
     - `../canvas-sp-cert.pem` → mounted to `/etc/ssl/certs/canvas-sp-cert.pem:ro`
   - **Certificate Authority:**
     - `../ca-cert.pem` → mounted to `/etc/ssl/certs/ca-cert.pem:ro`  
       *Also set the environment variable:*  
       `REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-cert.pem`
   - **Kerberos Configuration:**
     - `../krb5.keytab` → mounted to `/etc/krb5.keytab:ro`
     - `../krb5.conf` → mounted to `/etc/krb5.conf:ro`
   - **Canvas SAML:**
     - `../canvas-saml.crt` → mounted to `/etc/ssl/certs/canvas-saml.crt:ro`
     - `../canvas-saml.key` → mounted to `/etc/ssl/private/canvas-saml.key:ro`
   - **NGINX (for Canvas LMS):**
     - `../server.crt` → mounted to `/etc/nginx/certs/server.crt`
     - `../server.key` → mounted to `/etc/nginx/certs/server.key`

   *Make sure your Docker Compose configuration (typically `docker-compose.yml`) correctly references these files as volumes.*

4. **Build and Launch the Environment**

   Run the following command to build and start all containers in detached mode:
   ```bash
   docker-compose up -d --build
   ```

5. **Configure Canvas SAML Authentication**

   Once the containers are running, set up the Canvas SAML Authentication settings as required. The Docker Compose build automatically downloads and builds the latest production code for Canvas LMS.

---

## Current Features

- **User Authentication Using Kerberos:** Secure login leveraging Kerberos protocol.
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
- **Custom Degree Plans:** Inmates can explore and customize their degree paths based on personal interests and goals. A middle layer will be created for CTC Link, enabling students to apply for classes while adhering to DOC Policy 500, which prioritizes students closer to reentry.
- **Course Scheduling:** Automates class roster creation in CTC Link following DOC Policy 500, reducing manual administrative work.

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
