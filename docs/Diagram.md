
```flowchart TD
    A["Developer / AI Client"] -->|"POST /databases"| B["Backend API"]

    B --> C["Authentication"]
    C --> D["Authorization & Policy Engine"]
    D --> E{"Request allowed?"}

    E -->|No| F["403 Forbidden"]
    E -->|Yes| G["Provisioning Service"]

    G --> H["Kubernetes / Helm"]
    H --> I["PostgreSQL Instance"]

    G --> J["Metadata Store"]
    J --> K["Database status and ownership"]

    I --> L["Secure connection"]
    L --> M["Authorized consumer"]

    D -.-> N["Access policies"]
    N -.-> O["GRANT / REVOKE / RLS"]
```