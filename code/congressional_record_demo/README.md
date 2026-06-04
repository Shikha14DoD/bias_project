# Congressional Record Demo

## Purpose

Exploratory script to evaluate the Congressional Record (via GovInfo Bulk Data) 
as a supplementary corpus for the gender bias panel.

## Role in the project

Congressional Record is a Tier 2 supplementary source per the proposal. 
Primary intended use: **convergent validity check** on newspaper-derived 
bias scores. If bias scores from elite political speech (Congress) correlate 
with bias scores from mainstream press (newspapers) at the state-year level, 
that supports the construct validity of the measure.

Secondary potential use: partial fill for the 1964–1984 newspaper gap if 
TDM Studio access for ProQuest Historical Newspapers doesn't materialize.

## Coverage

- **GovInfo bulk XML**: 1994–present (clean computational access)
- **Pre-1994**: requires HeinOnline or ProQuest Congressional 
  (pending NJIT librarian inquiry)

## Files

- `cr_test.ipynb` — exploratory notebook
- `README.md` — this file

## Decision criteria

Congressional Record is viable for this project if:
- [ ] GovInfo Bulk Data API works reliably for our use case
- [ ] Member-state mapping is parseable from the XML
- [ ] Per state-year volume is sufficient for meaningful bias measurement
- [ ] Pre-1994 access can be negotiated (for full panel coverage)

## Findings

(To be filled in after running the demo.)