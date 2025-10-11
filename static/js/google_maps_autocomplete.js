/**
 * Google Maps Places Autocomplete Integration
 *
 * This script enables Google Maps Places Autocomplete on address forms.
 * It automatically populates address, city, state, postal code, county, and coordinates
 * when a user selects a place from the autocomplete dropdown.
 *
 * Updated to use the modern PlaceAutocompleteElement API (2025)
 *
 * Usage:
 * 1. Include this script after the Google Maps API script
 * 2. Call initializeAddressAutocomplete() with field IDs
 *
 * Example:
 * <script>
 *   initializeAddressAutocomplete({
 *     addressField: 'id_location_address',
 *     cityField: 'id_location_city',
 *     stateField: 'id_location_state_code',
 *     postalCodeField: 'id_location_postal_code',
 *     countyField: 'id_location_county',
 *     latitudeField: 'id_location_latitude',
 *     longitudeField: 'id_location_longitude'
 *   });
 * </script>
 */

let autocompleteInstance = null;

/**
 * Initialize Google Maps Places Autocomplete on an address field
 * Uses the modern PlaceAutocompleteElement or falls back to classic Autocomplete
 * @param {Object} config - Configuration object with field IDs
 * @param {string} config.searchContainerId - ID of the container where the search input will be placed
 * @param {string} config.addressField - ID of the address input field (will be populated, not replaced)
 * @param {string} [config.cityField] - ID of the city input field
 * @param {string} [config.stateField] - ID of the state input field
 * @param {string} [config.postalCodeField] - ID of the postal code input field
 * @param {string} [config.countyField] - ID of the county input field
 * @param {string} [config.latitudeField] - ID of the latitude input field
 * @param {string} [config.longitudeField] - ID of the longitude input field
 */
async function initializeAddressAutocomplete(config) {
    // Wait for Google Maps API to be available
    if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
        console.warn('Google Maps API not loaded. Autocomplete will not be available.');
        return;
    }

    const searchContainer = document.getElementById(config.searchContainerId);
    if (!searchContainer) {
        console.error(`Search container with ID "${config.searchContainerId}" not found`);
        return;
    }

    const addressInput = document.getElementById(config.addressField);
    if (!addressInput) {
        console.error(`Address field with ID "${config.addressField}" not found`);
        return;
    }

    try {
        // Use the modern PlaceAutocompleteElement (recommended as of 2025)
        // Create the autocomplete element
        const placeAutocomplete = new google.maps.places.PlaceAutocompleteElement({
            componentRestrictions: { country: 'us' },
            requestedLanguage: 'en',
            requestedRegion: 'us'
        });

        // Apply styling
        placeAutocomplete.style.display = 'block';
        placeAutocomplete.style.width = '100%';

        // Clear container and add autocomplete element
        searchContainer.innerHTML = '';
        searchContainer.appendChild(placeAutocomplete);

        // Listen for place selection using the new gmp-select event (replaces gmp-placeselect)
        placeAutocomplete.addEventListener('gmp-select', async (event) => {
            try {
                // Get the placePrediction from the event
                const { placePrediction } = event;

                if (!placePrediction) {
                    return;
                }

                // Convert prediction to place and fetch details
                const place = placePrediction.toPlace();
                await place.fetchFields({
                    fields: ['displayName', 'formattedAddress', 'addressComponents', 'location']
                });

                if (!place.location) {
                    return;
                }

                // Clear all location fields first
                clearAddressFields(config);

                // Populate the address field (Address Line 1)
                const streetNumber = getAddressComponent(place.addressComponents, 'street_number');
                const route = getAddressComponent(place.addressComponents, 'route');
                const addressLine = `${streetNumber} ${route}`.trim() || place.formattedAddress?.split(',')[0] || '';
                addressInput.value = addressLine;

                // Populate city
                if (config.cityField) {
                    const city = getAddressComponent(place.addressComponents, 'locality') ||
                                getAddressComponent(place.addressComponents, 'sublocality_level_1');
                    const cityField = document.getElementById(config.cityField);
                    if (cityField && city) {
                        cityField.value = city;
                    }
                }

                // Populate state
                if (config.stateField) {
                    const state = getAddressComponent(place.addressComponents, 'administrative_area_level_1', 'short_name');
                    const stateField = document.getElementById(config.stateField);
                    if (stateField && state) {
                        stateField.value = state;
                    }
                }

                // Populate postal code
                if (config.postalCodeField) {
                    const postalCode = getAddressComponent(place.addressComponents, 'postal_code');
                    const postalCodeField = document.getElementById(config.postalCodeField);
                    if (postalCodeField && postalCode) {
                        postalCodeField.value = postalCode;
                    }
                }

                // Populate county
                if (config.countyField) {
                    const county = getAddressComponent(place.addressComponents, 'administrative_area_level_2');
                    const countyField = document.getElementById(config.countyField);
                    if (countyField && county) {
                        countyField.value = county;
                    }
                }

                // Populate coordinates
                if (place.location) {
                    if (config.latitudeField) {
                        const latField = document.getElementById(config.latitudeField);
                        if (latField) {
                            const lat = typeof place.location.lat === 'function' ? place.location.lat() : place.location.lat;
                            latField.value = lat.toFixed(7);
                        }
                    }
                    if (config.longitudeField) {
                        const lngField = document.getElementById(config.longitudeField);
                        if (lngField) {
                            const lng = typeof place.location.lng === 'function' ? place.location.lng() : place.location.lng;
                            lngField.value = lng.toFixed(7);
                        }
                    }
                }

                // Trigger change events on all populated fields
                triggerChangeEvents(config);

            } catch (error) {
                console.error('Error processing place selection:', error);
            }
        });

    } catch (error) {
        // Fall back on error
        console.error('Error with PlaceAutocompleteElement:', error);
        initializeFallbackInput(config, searchContainer);
    }
}

/**
 * Helper function to extract address component by type
 */
function getAddressComponent(addressComponents, type, nameType = 'long_name') {
    if (!addressComponents || !Array.isArray(addressComponents)) return '';

    for (const component of addressComponents) {
        if (component.types && component.types.includes(type)) {
            return component[nameType] || component.longText || component.shortText || '';
        }
    }
    return '';
}

/**
 * Fallback for when PlaceAutocompleteElement is not available
 * Creates a simple text input with instructions
 */
function initializeFallbackInput(config, searchContainer) {
    // Display a message in the search container
    searchContainer.innerHTML = '<p class="text-sm text-gray-500">Google Maps autocomplete is not available in your browser. Please enter your address manually in the fields below.</p>';

    console.warn('PlaceAutocompleteElement not available. Manual address entry required.');
}


/**
 * Clear all address fields
 * @param {Object} config - Configuration object with field IDs
 */
function clearAddressFields(config) {
    const fieldIds = [
        config.cityField,
        config.stateField,
        config.postalCodeField,
        config.countyField,
        config.latitudeField,
        config.longitudeField
    ];

    fieldIds.forEach(fieldId => {
        if (fieldId) {
            const field = document.getElementById(fieldId);
            if (field) field.value = '';
        }
    });
}

/**
 * Trigger change events on all populated fields
 * @param {Object} config - Configuration object with field IDs
 */
function triggerChangeEvents(config) {
    const fieldIds = [
        config.addressField,
        config.cityField,
        config.stateField,
        config.postalCodeField,
        config.countyField,
        config.latitudeField,
        config.longitudeField
    ];

    fieldIds.forEach(fieldId => {
        if (fieldId) {
            const field = document.getElementById(fieldId);
            if (field) {
                field.dispatchEvent(new Event('change', { bubbles: true }));
                field.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    });
}
