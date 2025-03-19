Requirements : https://roadmap.sh/projects/weather-api-wrapper-service 

Key points: 
-> 3rd party weather API to fetch data (using python requests)
-> cache using Redis

WHY ?

1. Standardization & Simplicity
Third-party weather APIs often have complex responses with a lot of unnecessary data. By building a wrapper API, you can:

Extract only the useful data your application needs.
Provide a simpler and consistent response format.
2. Vendor Flexibility
If your app relies directly on a third-party API, you’re locked in to that provider.
By using a wrapper, you can easily switch providers in the future without breaking your application.
You could even combine multiple APIs to improve reliability.
3. Rate Limiting & Caching
Many free weather APIs have strict rate limits.
A wrapper API can cache responses and reduce unnecessary API calls.
This speeds up responses and helps avoid hitting API limits.
4. Custom Logic & Features
The third-party API may not provide exactly what you need.
You can add custom logic, such as:
Converting units (e.g., °C to °F).
Providing custom alerts (e.g., "Carry an umbrella today!").
Merging data from multiple sources.
5. Security & API Key Protection
Instead of exposing the third-party API key on the frontend, your backend (wrapper API) hides it.
You can control who accesses the weather data via authentication.
6. Business & Monetization
If you're building a SaaS or a public API, a wrapper allows you to:
Implement subscription models.
Add request limits per user.
Charge for premium weather features.
7. Data Enrichment
Combine weather data with other datasets (e.g., traffic, pollution, events).
Provide AI-driven insights (e.g., "Likelihood of rain based on historical trends").