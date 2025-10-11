/**
 * Google Maps Places Autocomplete Integration
 *
 * This script enables Google Maps Places Autocomplete on address forms.
 * It automatically populates address, city, state, postal code, county, and coordinates
 * when a user selects a place from the autocomplete dropdown.
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
 * @param {Object} config - Configuration object with field IDs
 * @param {string} config.addressField - ID of the address input field
 * @param {string} [config.cityField] - ID of the city input field
 * @param {string} [config.stateField] - ID of the state input field
 * @param {string} [config.postalCodeField] - ID of the postal code input field
 * @param {string} [config.countyField] - ID of the county input field
 * @param {string} [config.latitudeField] - ID of the latitude input field
 * @param {string} [config.longitudeField] - ID of the longitude input field
 */
function initializeAddressAutocomplete(config) {
    // Wait for Google Maps API to be available
    if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
        console.warn('Google Maps API not loaded. Autocomplete will not be available.');
        return;
    }

    const addressInput = document.getElementById(config.addressField);
    if (!addressInput) {
        console.error(`Address field with ID "${config.addressField}" not found`);
        return;
    }

    // Initialize autocomplete
    autocompleteInstance = new google.maps.places.Autocomplete(addressInput, {
        types: ['address'],
        fields: ['address_components', 'geometry', 'formatted_address']
    });

    // Add visual indicator that autocomplete is active
    addressInput.setAttribute('placeholder', 'Start typing address...');
    addressInput.setAttribute('title', 'Google Maps autocomplete enabled. Start typing to see suggestions.');

    // Add a subtle visual indicator
    const existingClass = addressInput.className;
    addressInput.className = existingClass + ' google-autocomplete-enabled';

    // Listen for place selection
    autocompleteInstance.addListener('place_changed', function() {
        const place = autocompleteInstance.getPlace();

        if (!place.address_components) {
            console.warn('No address components found for selected place');
            return;
        }

        // Clear all fields first
        clearAddressFields(config);

        // Parse address components
        const addressComponents = parseAddressComponents(place.address_components);

        // Populate address field with formatted address
        if (config.addressField && place.formatted_address) {
            const addressField = document.getElementById(config.addressField);
            if (addressField) {
                // Use street number + route for the address field
                const streetNumber = addressComponents.street_number || '';
                const route = addressComponents.route || '';
                addressField.value = `${streetNumber} ${route}`.trim() || place.formatted_address.split(',')[0];
            }
        }

        // Populate city
        if (config.cityField && addressComponents.locality) {
            const cityField = document.getElementById(config.cityField);
            if (cityField) cityField.value = addressComponents.locality;
        }

        // Populate state
        if (config.stateField && addressComponents.administrative_area_level_1) {
            const stateField = document.getElementById(config.stateField);
            if (stateField) stateField.value = addressComponents.administrative_area_level_1;
        }

        // Populate postal code
        if (config.postalCodeField && addressComponents.postal_code) {
            const postalCodeField = document.getElementById(config.postalCodeField);
            if (postalCodeField) postalCodeField.value = addressComponents.postal_code;
        }

        // Populate county
        if (config.countyField && addressComponents.administrative_area_level_2) {
            const countyField = document.getElementById(config.countyField);
            if (countyField) countyField.value = addressComponents.administrative_area_level_2;
        }

        // Populate coordinates
        if (place.geometry && place.geometry.location) {
            if (config.latitudeField) {
                const latField = document.getElementById(config.latitudeField);
                if (latField) latField.value = place.geometry.location.lat().toFixed(7);
            }
            if (config.longitudeField) {
                const lngField = document.getElementById(config.longitudeField);
                if (lngField) lngField.value = place.geometry.location.lng().toFixed(7);
            }
        }

        // Trigger change events on all populated fields
        triggerChangeEvents(config);
    });

    console.log('Google Maps autocomplete initialized successfully');
}

/**
 * Parse Google Maps address components into a structured object
 * @param {Array} components - Array of address components from Google Maps
 * @returns {Object} Structured address data
 */
function parseAddressComponents(components) {
    const componentMap = {
        street_number: 'short_name',
        route: 'long_name',
        locality: 'long_name',
        administrative_area_level_1: 'short_name',
        administrative_area_level_2: 'long_name',
        country: 'short_name',
        postal_code: 'short_name'
    };

    const result = {};

    components.forEach(component => {
        const type = component.types[0];
        if (componentMap[type]) {
            result[type] = component[componentMap[type]];
        }
    });

    return result;
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
