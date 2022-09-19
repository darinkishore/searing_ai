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
import type { Question } from './Question';
import {
    QuestionFromJSON,
    QuestionFromJSONTyped,
    QuestionToJSON,
} from './Question';

/**
 * 
 * @export
 * @interface PaginatedQuestionList
 */
export interface PaginatedQuestionList {
    /**
     * 
     * @type {number}
     * @memberof PaginatedQuestionList
     */
    count?: number;
    /**
     * 
     * @type {string}
     * @memberof PaginatedQuestionList
     */
    next?: string | null;
    /**
     * 
     * @type {string}
     * @memberof PaginatedQuestionList
     */
    previous?: string | null;
    /**
     * 
     * @type {Array<Question>}
     * @memberof PaginatedQuestionList
     */
    results?: Array<Question>;
}

/**
 * Check if a given object implements the PaginatedQuestionList interface.
 */
export function instanceOfPaginatedQuestionList(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function PaginatedQuestionListFromJSON(json: any): PaginatedQuestionList {
    return PaginatedQuestionListFromJSONTyped(json, false);
}

export function PaginatedQuestionListFromJSONTyped(json: any, ignoreDiscriminator: boolean): PaginatedQuestionList {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'count': !exists(json, 'count') ? undefined : json['count'],
        'next': !exists(json, 'next') ? undefined : json['next'],
        'previous': !exists(json, 'previous') ? undefined : json['previous'],
        'results': !exists(json, 'results') ? undefined : ((json['results'] as Array<any>).map(QuestionFromJSON)),
    };
}

export function PaginatedQuestionListToJSON(value?: PaginatedQuestionList | null): any {
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
        'results': value.results === undefined ? undefined : ((value.results as Array<any>).map(QuestionToJSON)),
    };
}

