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
import type { DepartmentEnum } from './DepartmentEnum';
import {
    DepartmentEnumFromJSON,
    DepartmentEnumFromJSONTyped,
    DepartmentEnumToJSON,
} from './DepartmentEnum';

/**
 * 
 * @export
 * @interface Employee
 */
export interface Employee {
    /**
     * 
     * @type {number}
     * @memberof Employee
     */
    readonly id: number;
    /**
     * 
     * @type {number}
     * @memberof Employee
     */
    readonly user: number;
    /**
     * Your employee's name.
     * @type {string}
     * @memberof Employee
     */
    name: string;
    /**
     * 
     * @type {DepartmentEnum}
     * @memberof Employee
     */
    department: DepartmentEnum;
    /**
     * Your employee's annual salary.
     * @type {number}
     * @memberof Employee
     */
    salary: number;
    /**
     * 
     * @type {Date}
     * @memberof Employee
     */
    readonly createdAt: Date;
    /**
     * 
     * @type {Date}
     * @memberof Employee
     */
    readonly updatedAt: Date;
}

/**
 * Check if a given object implements the Employee interface.
 */
export function instanceOfEmployee(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "user" in value;
    isInstance = isInstance && "name" in value;
    isInstance = isInstance && "department" in value;
    isInstance = isInstance && "salary" in value;
    isInstance = isInstance && "createdAt" in value;
    isInstance = isInstance && "updatedAt" in value;

    return isInstance;
}

export function EmployeeFromJSON(json: any): Employee {
    return EmployeeFromJSONTyped(json, false);
}

export function EmployeeFromJSONTyped(json: any, ignoreDiscriminator: boolean): Employee {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'user': json['user'],
        'name': json['name'],
        'department': DepartmentEnumFromJSON(json['department']),
        'salary': json['salary'],
        'createdAt': (new Date(json['created_at'])),
        'updatedAt': (new Date(json['updated_at'])),
    };
}

export function EmployeeToJSON(value?: Employee | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'name': value.name,
        'department': DepartmentEnumToJSON(value.department),
        'salary': value.salary,
    };
}

