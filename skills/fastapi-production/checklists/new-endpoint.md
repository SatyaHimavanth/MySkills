# New Endpoint Checklist

- [ ] Existing endpoint pattern reviewed
- [ ] Correct HTTP method chosen
- [ ] Request model added
- [ ] Response model added
- [ ] Examples/descriptions added
- [ ] Authentication handled
- [ ] Authorization handled
- [ ] Multi-tenant scoping reviewed if applicable (`database/multi_tenancy.shared.md`)
- [ ] Audit log entry added if this endpoint mutates state a compliance/support trail needs (`security/audit_logging.shared.md`)
- [ ] Status codes defined
- [ ] Pagination or limits defined if needed
- [ ] Transaction behavior reviewed
- [ ] Error contract updated
- [ ] OpenAPI documentation remains clear
- [ ] Tests added
