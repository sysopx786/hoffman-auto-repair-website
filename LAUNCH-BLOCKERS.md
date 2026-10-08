# LAUNCH BLOCKERS

Nothing below is published. Resolve each item with Dave, then update `src/services.json` and run `python3 src/build.py`.

## 1. Business facts to confirm

- [ ] Primary phone: 484-921-0715 (site) vs (610) 935-1103 (shown on Contact only). Is one a tracking number? Edit `src/site.config.json`.
- [ ] Inspection vehicle categories (cars, motorcycles, trucks, trailers). Site says only: "OBD emissions testing and trailer inspections. Call to confirm we can inspect your vehicle type." Several FAQs still say "we are an official PennDOT inspection station" and imply car inspections; reword once confirmed.
- [ ] Inspection and emissions price, retest policy, whether fees are posted at the shop (site says fees are posted).
- [ ] Towing area, 24/7 or business hours, after-hours number, pricing approach.
- [ ] Licensing and insurance for towing, repossession, impound, parking enforcement and surveillance. Not researched. Consider a lawyer review. Remove anything Dave does not do today.
- [ ] Property & Parking wording, Salvage Keys Made, Retreads, Storage Shed Moving, Gas Tanks, Collision Services scope.
- [ ] "Routine maintenance" on Home: brakes, alignment, A/C, batteries, oil changes are not on the service list.
- [ ] "Family-run" and "fair pricing" claims; "Dave and Mel" relationship.
- [ ] Review wording, reviewer names, permission to publish. Live Google rating and count (site shows neither; no AggregateRating schema). Google review link: set `googleReviewUrl` in config.
- [ ] Email dmkrhoff@dplus.net: not on the site. Add only if Dave wants it public.
- [ ] EPA certification for A/C refrigerant handling (Freon & Coolant Recycling).
- [ ] Owner words, opening year (unverified ~1986), Mel's role for About.

## 2. Assets

- [ ] Photos: shop exterior, Dave, team, bays (About page has empty slots; `showPhotoComingLabel` in config).
- [ ] Service-page images (`assets/img/svc/`, mapped in `src/images.json`) are generic illustrations, not photos of Dave's shop. Swap for real photos or keep, and confirm Dave is fine with them. EV charging image held back until Dave confirms EV service.
- [ ] Original vector logo. The flat SVG is traced from the 2576px raster; ask Dave or the sign maker for the source.

## 3. Deployment

- [ ] Replace `REPLACE-WITH-DOMAIN` in `src/site.config.json`, rebuild. Canonical, OG, sitemap and schema use it.
- [ ] 404.html uses `<base href="/">`: works on a custom domain at root, not on a project path.
- [ ] After launch: claim Birdeye and PA inspection listings; match name, phone, hours.

## 4. FAQs excluded from page and schema (31)

### Inspections & Emissions
- **Emissions Testing** — Do I need an emissions test? _(source note: [Likely] Many southeast PA counties require it. Check your renewal notice.)_
- **Pre-Purchase Inspections** — Can you inspect at the seller's location? _(source note: [Dave to confirm.])_

### Towing & Hauling
- **Rollback Towing** — Is it more costly than a hook tow? _(source note: [Dave to confirm.])_
- **Long Distance Towing** — How is it priced? _(source note: [Dave to confirm.] Distance is a large factor.)_
- **Long Distance Towing** — Can I ride along? _(source note: [Dave to confirm.])_
- **Insurance Towing** — Can you bill my insurer? _(source note: [Dave to confirm.])_

### Roadside & Recovery
- **Roadside Assistance** — Are you available nights and weekends? _(source note: [Dave to confirm after-hours service.] The shop is closed Sat-Sun.)_

### Property, Parking & Impound
- **Parking Enforcement** — Is a written agreement needed? _(source note: [Dave to confirm.] Many properties use one.)_
- **Parking Lot Enforcement** — Is a contract needed? _(source note: [Dave to confirm.])_
- **Parking Lot Surveillance** — What does surveillance include? _(source note: [Dave to define scope.])_
- **Parking Lot Surveillance** — Is it camera monitoring? _(source note: [Dave to confirm.])_
- **Parking Lot Surveillance** — Do you work nights? _(source note: [Dave to confirm.])_
- **Impound Services** — What are your fees? _(source note: [Dave to confirm.])_
- **Vehicle Storage** — How long can I leave a vehicle? _(source note: [Dave to confirm limits.] Call to set terms.)_
- **Vehicle Storage** — Is storage indoors or outdoors? _(source note: [Dave to confirm.])_
- **Vehicle Storage** — What does storage cost? _(source note: [Dave to confirm rates.] Call for current pricing.)_

### Recycling & Salvage
- **Battery Recycling** — Do you take batteries I didn't buy from you? _(source note: [Dave to confirm policy.] Call before you drop one off.)_
- **Battery Recycling** — Will I get anything for my old battery? _(source note: [Dave to confirm: core credit or fee.] Ask when you call.)_
- **Oil Recycling** — Can I bring oil from home changes? _(source note: [Dave to confirm.])_
- **Oil Recycling** — Is there a fee? _(source note: [Dave to confirm.])_
- **Tire Recycling** — Can I drop off old tires? _(source note: [Dave to confirm.] Call first.)_
- **Tire Recycling** — Is there a fee? _(source note: [Dave to confirm.] Ask when you call.)_
- **Tire Recycling** — How many tires can I bring? _(source note: [Dave to confirm limits.])_
- **Freon & Coolant Recycling** — Can I bring in old coolant? _(source note: [Dave to confirm.] Call first.)_
- **Junk Car Removal** — Do you buy junk cars? _(source note: [Dave to confirm.] Call to ask.)_

### Tires, Wheels & Suspension
- **Tires** — Do you offer all brands? _(source note: [Dave to confirm.])_
- **Tires** — Do you balance? _(source note: [Dave to confirm.])_
- **Tire Rotation** — Will you check pressure and tread? _(source note: [Dave to confirm.] Ask when booking.)_
- **Wheels** — Do you stock wheels? _(source note: [Dave to confirm.] We can often source them.)_
- **Wheel Repair** — Does wheel repair include balancing? _(source note: [Dave to confirm.] Balancing is normally needed after repair.)_

### Body, Glass & Imports
- **Imports** — Which import brands do you service? _(source note: [Dave to list brands.] Call to ask.)_
