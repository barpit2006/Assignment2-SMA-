## Investigation Notes — CoA Architect Directory Search

Before building the extraction pipeline, I explored how the Council of 
Architecture's directory search actually works, as required by the 
assignment brief.

### Entry point

The main directory page is:

https://coa.gov.in/search_arch.php?lang=1&level=1&linkid=&lid=289&lang=1


This isn't a search form itself — it's a menu of search modes: Name, 
Registration Number, Year of Registration, State, City, and Pincode. 
Each mode links out using a `searCat` parameter in the URL (e.g. Name 
search uses `searCat=1`).

### Testing the "Search By Name" flow

Used a well-known architect's name (Balkrishna Vithaldas Doshi) to 
maximize the chance of hitting a real record. This led to:

https://coa.gov.in/search_architectResult.php?lang=1&level=1&linkid=&lid=289


Notably, the searched name does **not** appear anywhere in the URL, 
even though the page clearly used it (the results header reads 
*"Architect's List Based on [Balkrishna Vithaldas Doshi] Architect Name 
wise Search"*). This indicates the search term is submitted via a 
**POST** request rather than GET — confirmed via Chrome DevTools → 
Network tab, where the request appears as a POST to 
`search_architectResult.php`.

### Result fields exposed

The results table has these columns:

| S.No | Architect Name | Registration Number | Disciplinary Action | Address | Mobile | Email ID |
|------|-----------------|----------------------|----------------------|---------|--------|----------|

This tells us the data schema the system is designed around, regardless 
of whether we can see actual values.

### Key finding: access is deliberately gated

Despite the search executing correctly, the table returned 
**"No Record(s) Available"**, followed by:

> *"To View further you are required to Login and purchase an Online 
> Directory, 'Click Here' to Proceed!"*

Combined with the homepage's earlier notice that unauthenticated users 
get **3 free searches per day per IP**, this confirms the restriction 
is intentional and enforced server-side — not a technical bug or a 
simple soft rate limit.

### Conclusion / scoping decision

Because full-scale data is deliberately gated behind a paid 
login/subscription, this project does **not** attempt large-scale live 
extraction against the real site. Instead:

- The full pipeline (queue table, retry/backoff, resumability, 
  duplicate detection, login-wall/CAPTCHA detection, progress 
  dashboard) is built and demonstrated against a small number of 
  legitimately-accessible lookups.
- A synthetic dataset matching the real schema is used to demonstrate 
  the pipeline operating at scale (thousands of records), since the 
  live site does not permit that volume of access without a paid 
  subscription.
