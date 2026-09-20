# Overflow Dashboard

Overflow includes a lightweight local dashboard.

It is served directly by the gateway and uses no external CDN dependencies.

## Run the dashboard

Start the gateway and open the dashboard automatically:

```powershell
powershell -File scripts\open_dashboard.ps1
```

Or start the gateway manually:

```powershell
python -m overflow.cli gateway
```

Then open:

```text
http://127.0.0.1:8080/dashboard
```

## Dashboard features

- Live gateway health indicator
- Privacy check tester
- Security scan tester
- Pipeline chat tester
- Optimizer tester

The dashboard is local-only by default.
