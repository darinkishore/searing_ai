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
import type { Summary } from './Summary';
import {
    SummaryFromJSON,
    SummaryFromJSONTyped,
    SummaryToJSON,
} from './Summary';

/**
 * 
 * @export
 * @interface PaginatedSummaryList
 */
export interface PaginatedSummaryList {
    /**
     * 
     * @type {number}
     * @memberof PaginatedSummaryList
     */
    count?: number;
    /**
     * 
     * @type {string}
     * @memberof PaginatedSummaryList
     */
    next?: string | null;
    /**
     * 
     * @type {string}
     * @memberof PaginatedSummaryList
     */
    previous?: string | null;
    /**
     * 
     * @type {Array<Summary>}
     * @memberof PaginatedSummaryList
     */
    results?: Array<Summary>;
}

/**
 * Check if a given object implements the PaginatedSummaryList interface.
 */
export function instanceOfPaginatedSummaryList(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function PaginatedSummaryListFromJSON(json: any): PaginatedSummaryList {
    return PaginatedSummaryListFromJSONTyped(json, false);
}

export function PaginatedSummaryListFromJSONTyped(json: any, ignoreDiscriminator: boolean): PaginatedSummaryList {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'count': !exists(json, 'count') ? undefined : json['count'],
        'next': !exists(json, 'next') ? undefined : json['next'],
        'previous': !exists(json, 'previous') ? undefined : json['previous'],
        'results': !exists(json, 'results') ? undefined : ((json['results'] as Array<any>).map(SummaryFromJSON)),
    };
}

export function PaginatedSummaryListToJSON(value?: PaginatedSummaryList | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'count': value.count,
        'next': value.next,
        'previous': value.previous,
        'results': value.results === undefined ? undefined : ((value.results as Array<any>).map(SummaryToJSON)),
    };
}
