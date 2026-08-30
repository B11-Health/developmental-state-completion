# F3 Source and Browser-State Audit

Date: 2026-08-30

## Live browser findings

- `https://www.research.gov/research-web/` loaded the official Research.gov home page and displayed **Sign In Register**. This is anonymous/public state.
- Following **Sign In** navigated to the official NSF authentication endpoint on `https://external.nsf.gov/...` with title **Research.gov - Sign In**. No authenticated Research.gov dashboard or organization context was available.
- `https://apps.research.gov/account/registration` displayed the individual **Account Registration** form. It states that each individual should not have more than one NSF ID and includes a required age confirmation plus **Save & Preview**. F3 did not enter data or create an account.
- `https://www.research.gov/research-web/content/aboutacctmgmt` states that registration with NSF at both organization and individual levels is required for proposal/post-award activity and that role-based activity requires an NSF account plus an **organization-approved role such as Principal Investigator (PI) or Authorized Organizational Representative (AOR)**.
- A public Research.gov legacy help page (`https://resources.research.gov/common/robohelp/public/WebHelp/Research_gov_Registration.htm`) describes Institution Administrator-controlled assignment of PI/SPO roles. Because parts of that page still reference DUNS/CCR/FastLane, F3 uses it only as historical/procedural context and defers to the current Account Management page/PAPPG for present requirements.

## Repository evidence inherited from F2/current main

- `FUNDING_PIPELINE.md` and `grants/SUBMISSION_READINESS.md` record SAM activation on 2026-08-19 and renewal 2027-08-19.
- The repository intentionally excludes UEI/CAGE/EIN and other sensitive identifiers.
- Prior mailbox audit did not surface an IRS determination letter.
- F2 left Research.gov organization registration, PI/AOR/SPO roles, COI, disclosures, and F&A treatment unresolved.

## Interpretation discipline

Anonymous browser state is **not evidence that an account or organization does not exist**. It only disproves the narrower proposition that this controlled browser session is currently authenticated into Research.gov. Therefore organization existence, UEI linkage, and role status remain unresolved until an authorized account holder signs in and exposes the organization/account-management state.
