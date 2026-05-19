## Nytt dbt prosjekt

### Oppsett
- Gi navn til prosjektet i dbt_project.yml
- Opprett en profil i profiles.yml og referer til profilen i dbt_project.yml


For å kjøre dbt prosjektet fra utviklerimage må dbt ha tilgang til secrets for:
- miljø (Spesifisert i profiles.yml)
- komponentskjema
- personlig brukernavn
- personlig passord

Disse secretene settes opp med skriptet [setup_db_user.ps1](https://github.com/navikt/dbt-i-nav/blob/main/start_vscode_dbt.ps1) (for VDI) eller [start_vscode_dbt_laptop.ps1](https://github.com/navikt/dbt-i-nav/blob/main/start_vscode_dbt.ps1) (for dbt rett fra egen laptop), som setter dem som miljøvariabler. Skriptet kjøres fra snarvei som det finnes [egen oppskrift på](https://navikt.github.io/dbt-i-nav/Installasjon-p%C3%A5-VDI/dbt-power-user/).

### Schedulering

dbt_run.py er et skript for schedulere dbt prosjektet i Airflow. Denne filen må endres til å passe sammen med secrets håndteringen til teamet.
Denne løsningen er underutfasing til fordel for en egen dbt_operator innebygd i dataverk.

### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
