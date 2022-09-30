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
 * @interface Question
 */
export interface Question {
    /**
     * 
     * @type {number}
     * @memberof Question
     */
    readonly id: number;
    /**
     * 
     * @type {string}
     * @memberof Question
     */
    readonly document: string | null;
    /**
     * 
     * @type {string}
     * @memberof Question
     */
    question?: string;
    /**
     * 
     * @type {string}
     * @memberof Question
     */
    answer?: string;
    /**
     * 
     * @type {Date}
     * @memberof Question
     */
    readonly createdAt: Date;
    /**
     * 
     * @type {Date}
     * @memberof Question
     */
    readonly updatedAt: Date;
}

/**
 * Check if a given object implements the Question interface.
 */
export function instanceOfQuestion(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "document" in value;
    isInstance = isInstance && "createdAt" in value;
    isInstance = isInstance && "updatedAt" in value;

    return isInstance;
}

export function QuestionFromJSON(json: any): Question {
    return QuestionFromJSONTyped(json, false);
}

export function QuestionFromJSONTyped(json: any, ignoreDiscriminator: boolean): Question {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'document': json['document'],
        'question': !exists(json, 'question') ? undefined : json['question'],
        'answer': !exists(json, 'answer') ? undefined : json['answer'],
        'createdAt': (new Date(json['created_at'])),
        'updatedAt': (new Date(json['updated_at'])),
    };
}

export function QuestionToJSON(value?: Question | null): any {
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

