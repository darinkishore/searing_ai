/* tslint:disable */
/* eslint-disable */
/**
 * Searing.ai
 * Learn shit. Real fast.
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface DocumentForm
 */
export interface DocumentForm {
    /**
     * 
     * @type {string}
     * @memberof DocumentForm
     */
    file?: string;
    /**
     * 
     * @type {string}
     * @memberof DocumentForm
     */
    title?: string;
}

/**
 * Check if a given object implements the DocumentForm interface.
 */
export function instanceOfDocumentForm(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function DocumentFormFromJSON(json: any): DocumentForm {
    return DocumentFormFromJSONTyped(json, false);
}

export function DocumentFormFromJSONTyped(json: any, ignoreDiscriminator: boolean): DocumentForm {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'file': !exists(json, 'file') ? undefined : json['file'],
        'title': !exists(json, 'title') ? undefined : json['title'],
    };
}

export function DocumentFormToJSON(value?: DocumentForm | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'file': value.file,
        'title': value.title,
    };
}

