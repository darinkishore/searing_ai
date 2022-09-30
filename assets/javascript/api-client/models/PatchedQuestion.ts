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
 * @interface PatchedQuestion
 */
export interface PatchedQuestion {
    /**
     * 
     * @type {number}
     * @memberof PatchedQuestion
     */
    readonly id?: number;
    /**
     * 
     * @type {string}
     * @memberof PatchedQuestion
     */
    readonly document?: string | null;
    /**
     * 
     * @type {string}
     * @memberof PatchedQuestion
     */
    question?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedQuestion
     */
    answer?: string;
    /**
     * 
     * @type {Date}
     * @memberof PatchedQuestion
     */
    readonly createdAt?: Date;
    /**
     * 
     * @type {Date}
     * @memberof PatchedQuestion
     */
    readonly updatedAt?: Date;
}

/**
 * Check if a given object implements the PatchedQuestion interface.
 */
export function instanceOfPatchedQuestion(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function PatchedQuestionFromJSON(json: any): PatchedQuestion {
    return PatchedQuestionFromJSONTyped(json, false);
}

export function PatchedQuestionFromJSONTyped(json: any, ignoreDiscriminator: boolean): PatchedQuestion {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': !exists(json, 'id') ? undefined : json['id'],
        'document': !exists(json, 'document') ? undefined : json['document'],
        'question': !exists(json, 'question') ? undefined : json['question'],
        'answer': !exists(json, 'answer') ? undefined : json['answer'],
        'createdAt': !exists(json, 'created_at') ? undefined : (new Date(json['created_at'])),
        'updatedAt': !exists(json, 'updated_at') ? undefined : (new Date(json['updated_at'])),
    };
}

export function PatchedQuestionToJSON(value?: PatchedQuestion | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'question': value.question,
        'answer': value.answer,
    };
}
