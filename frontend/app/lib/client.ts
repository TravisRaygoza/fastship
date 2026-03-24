/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** TagName */
export enum TagName {
  Express = "express",
  Standard = "standard",
  Fragile = "fragile",
  Heavy = "heavy",
  International = "international",
  Domestic = "domestic",
  TemperatureControlled = "temperature_controlled",
  Gift = "gift",
  Return = "return",
  Documents = "documents",
}

/** ShipmentStatus */
export enum ShipmentStatus {
  Placed = "placed",
  InTransit = "in_transit",
  OutForDelivery = "out_for_delivery",
  Delivered = "delivered",
  Cancelled = "cancelled",
}

/** Body_login_delivery_partner_partner_token_post */
export interface BodyLoginDeliveryPartnerPartnerTokenPost {
  /** Grant Type */
  grant_type?: string | null;
  /** Username */
  username: string;
  /**
   * Password
   * @format password
   */
  password: string;
  /**
   * Scope
   * @default ""
   */
  scope?: string;
  /** Client Id */
  client_id?: string | null;
  /**
   * Client Secret
   * @format password
   */
  client_secret?: string | null;
}

/** Body_login_seller_seller_token_post */
export interface BodyLoginSellerSellerTokenPost {
  /** Grant Type */
  grant_type?: string | null;
  /** Username */
  username: string;
  /**
   * Password
   * @format password
   */
  password: string;
  /**
   * Scope
   * @default ""
   */
  scope?: string;
  /** Client Id */
  client_id?: string | null;
  /**
   * Client Secret
   * @format password
   */
  client_secret?: string | null;
}

/** Body_reset_password_seller_reset_password_post */
export interface BodyResetPasswordSellerResetPasswordPost {
  /** Password */
  password: string;
}

/** Body_submit_review_shipments_review_post */
export interface BodySubmitReviewShipmentsReviewPost {
  /**
   * Rating
   * @min 1
   * @max 5
   */
  rating: number;
  /** Comment */
  comment: string | null;
}

/** DeliveryPartnerCreate */
export interface DeliveryPartnerCreate {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Serviceable Zip Codes */
  serviceable_zip_codes: number[];
  /** Max Handling Capacity */
  max_handling_capacity: number;
  /** Password */
  password: string;
}

/** DeliveryPartnerRead */
export interface DeliveryPartnerRead {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Serviceable Zip Codes */
  serviceable_zip_codes: number[];
  /** Max Handling Capacity */
  max_handling_capacity: number;
}

/** DeliveryPartnerUpdate */
export interface DeliveryPartnerUpdate {
  /** Serviceable Zip Codes */
  serviceable_zip_codes?: number[] | null;
  /** Max Handling Capacity */
  max_handling_capacity?: number | null;
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/** Seller */
export interface Seller {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /**
   * Email Verified
   * @default false
   */
  email_verified?: boolean;
  /**
   * Id
   * @format uuid
   */
  id: string;
  /**
   * Created At
   * @format date-time
   */
  created_at: string;
  /** Address */
  address?: string | null;
  /** Zip Code */
  zip_code?: number | null;
}

/** SellerCreate */
export interface SellerCreate {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Password */
  password: string;
}

/** SellerRead */
export interface SellerRead {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
}

/** ShipmentCreate */
export interface ShipmentCreate {
  /**
   * Content
   * Content of the shipment
   * @maxLength 50
   */
  content: string;
  /**
   * Weight
   * Weight of the shipment in lbs
   * @min 0.5
   * @exclusiveMax 50
   */
  weight: number;
  /**
   * Destination
   * Destination zip code of the shipment
   */
  destination: number;
  /**
   * Client Contact Email
   * Contact email of the client
   */
  client_contact_email: string | null;
  /**
   * Client Contact Phone
   * Contact phone number of the client
   */
  client_contact_phone?: string | null;
}

/** ShipmentEvent */
export interface ShipmentEvent {
  /**
   * Id
   * @format uuid
   */
  id: string;
  /**
   * Created At
   * @format date-time
   */
  created_at: string;
  /** Location Zipcode */
  location_zipcode: number;
  status: ShipmentStatus;
  /** Description */
  description?: string | null;
  /**
   * Shipment Id
   * @format uuid
   */
  shipment_id: string;
}

/** ShipmentRead */
export interface ShipmentRead {
  /**
   * Content
   * Content of the shipment
   * @maxLength 50
   */
  content: string;
  /**
   * Weight
   * Weight of the shipment in lbs
   * @min 0.5
   * @exclusiveMax 50
   */
  weight: number;
  /**
   * Destination
   * Destination zip code of the shipment
   */
  destination: number;
  /**
   * Id
   * @format uuid
   */
  id: string;
  seller: Seller;
  /**
   * Timeline
   * @default []
   */
  timeline?: ShipmentEvent[];
  /**
   * Estimated Delivery
   * @format date-time
   */
  estimated_delivery: string;
  /**
   * Tags
   * List of tags associated with the shipment
   */
  tags?: Tag[];
}

/** ShipmentUpdate */
export interface ShipmentUpdate {
  /**
   * Location
   * Current location zip code of the shipment
   */
  location?: number | null;
  /**
   * Description
   * Description of the shipment status
   */
  description?: string | null;
  /** Current status of the shipment */
  status?: ShipmentStatus | null;
  /**
   * Verification Code
   * Verification code for delivery confirmation
   */
  verification_code?: string | null;
  /**
   * Estimated Delivery
   * Estimated delivery date of the shipment
   */
  estimated_delivery?: string | null;
}

/** Tag */
export interface Tag {
  /**
   * Id
   * @format uuid
   */
  id: string;
  name: TagName;
  /** Instruction */
  instruction: string;
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
}

import type {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  HeadersDefaults,
  ResponseType,
} from "axios";
import axios from "axios";

export type QueryParamsType = Record<string | number, any>;

export interface FullRequestParams
  extends Omit<AxiosRequestConfig, "data" | "params" | "url" | "responseType"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseType;
  /** request body */
  body?: unknown;
}

export type RequestParams = Omit<
  FullRequestParams,
  "body" | "method" | "query" | "path"
>;

export interface ApiConfig<SecurityDataType = unknown>
  extends Omit<AxiosRequestConfig, "data" | "cancelToken"> {
  securityWorker?: (
    securityData: SecurityDataType | null,
  ) => Promise<AxiosRequestConfig | void> | AxiosRequestConfig | void;
  secure?: boolean;
  format?: ResponseType;
}

export enum ContentType {
  Json = "application/json",
  JsonApi = "application/vnd.api+json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public instance: AxiosInstance;
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private secure?: boolean;
  private format?: ResponseType;

  constructor({
    securityWorker,
    secure,
    format,
    ...axiosConfig
  }: ApiConfig<SecurityDataType> = {}) {
    this.instance = axios.create({
      ...axiosConfig,
      baseURL: axiosConfig.baseURL || "",
    });
    this.secure = secure;
    this.format = format;
    this.securityWorker = securityWorker;
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected mergeRequestParams(
    params1: AxiosRequestConfig,
    params2?: AxiosRequestConfig,
  ): AxiosRequestConfig {
    const method = params1.method || (params2 && params2.method);

    return {
      ...this.instance.defaults,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...((method &&
          this.instance.defaults.headers[
            method.toLowerCase() as keyof HeadersDefaults
          ]) ||
          {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected stringifyFormItem(formItem: unknown) {
    if (typeof formItem === "object" && formItem !== null) {
      return JSON.stringify(formItem);
    } else {
      return `${formItem}`;
    }
  }

  protected createFormData(input: Record<string, unknown>): FormData {
    if (input instanceof FormData) {
      return input;
    }
    return Object.keys(input || {}).reduce((formData, key) => {
      const property = input[key];
      const propertyContent: any[] =
        property instanceof Array ? property : [property];

      for (const formItem of propertyContent) {
        const isFileType = formItem instanceof Blob || formItem instanceof File;
        formData.append(
          key,
          isFileType ? formItem : this.stringifyFormItem(formItem),
        );
      }

      return formData;
    }, new FormData());
  }

  public request = async <T = any, _E = any>({
    secure,
    path,
    type,
    query,
    format,
    body,
    ...params
  }: FullRequestParams): Promise<AxiosResponse<T>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const responseFormat = format || this.format || undefined;

    if (
      type === ContentType.FormData &&
      body &&
      body !== null &&
      typeof body === "object"
    ) {
      body = this.createFormData(body as Record<string, unknown>);
    }

    if (
      type === ContentType.Text &&
      body &&
      body !== null &&
      typeof body !== "string"
    ) {
      body = JSON.stringify(body);
    }

    return this.instance.request({
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type ? { "Content-Type": type } : {}),
      },
      params: query,
      responseType: responseFormat,
      data: body,
      url: path,
    });
  };
}

/**
 * @title FastAPI
 * @version 0.1.0
 */
export class Api<
  SecurityDataType extends unknown,
> extends HttpClient<SecurityDataType> {
  /**
   * No description
   *
   * @name ReadRootGet
   * @summary Read Root
   * @request GET:/
   */
  readRootGet = (params: RequestParams = {}) =>
    this.request<any, any>({
      path: `/`,
      method: "GET",
      format: "json",
      ...params,
    });

  shipments = {
    /**
     * No description
     *
     * @tags shipments
     * @name GetTrackingShipmentsTrackGet
     * @summary Get Tracking
     * @request GET:/shipments/track
     */
    getTrackingShipmentsTrackGet: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/shipments/track`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipments
     * @name GetShipmentsWithTagShipmentsTaggedGet
     * @summary Get Shipments With Tag
     * @request GET:/shipments/tagged
     */
    getShipmentsWithTagShipmentsTaggedGet: (
      query: {
        tag_name: TagName;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead[], HTTPValidationError>({
        path: `/shipments/tagged`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipments
     * @name AddTagToShipmentShipmentsTagGet
     * @summary Add Tag To Shipment
     * @request GET:/shipments/tag
     */
    addTagToShipmentShipmentsTagGet: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
        tag: TagName;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipments/tag`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipments
     * @name RemoveTagFromShipmentShipmentsTagDelete
     * @summary Remove Tag From Shipment
     * @request DELETE:/shipments/tag
     */
    removeTagFromShipmentShipmentsTagDelete: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
        tag: TagName;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipments/tag`,
        method: "DELETE",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipments
     * @name SubmitReviewPageShipmentsReviewGet
     * @summary Submit Review Page
     * @request GET:/shipments/review
     */
    submitReviewPageShipmentsReviewGet: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/shipments/review`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipments
     * @name SubmitReviewShipmentsReviewPost
     * @summary Submit Review
     * @request POST:/shipments/review
     */
    submitReviewShipmentsReviewPost: (
      query: {
        /** Token */
        token: string;
      },
      data: BodySubmitReviewShipmentsReviewPost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/shipments/review`,
        method: "POST",
        query: query,
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipments
     * @name SubmitShipmentShipmentsPost
     * @summary Submit Shipment
     * @request POST:/shipments/
     * @secure
     */
    submitShipmentShipmentsPost: (
      data: ShipmentCreate,
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipments/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipments
     * @name GetShipmentShipmentsIdGet
     * @summary Get Shipment
     * @request GET:/shipments/{id}
     * @secure
     */
    getShipmentShipmentsIdGet: (id: string, params: RequestParams = {}) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipments/${id}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipments
     * @name ShipmentUpdateShipmentsIdPatch
     * @summary Shipment Update
     * @request PATCH:/shipments/{id}
     * @secure
     */
    shipmentUpdateShipmentsIdPatch: (
      id: string,
      data: ShipmentUpdate,
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipments/${id}`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipments
     * @name DeleteShipmentShipmentsIdDelete
     * @summary Delete Shipment
     * @request DELETE:/shipments/{id}
     * @secure
     */
    deleteShipmentShipmentsIdDelete: (id: string, params: RequestParams = {}) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipments/${id}`,
        method: "DELETE",
        secure: true,
        format: "json",
        ...params,
      }),
  };
  seller = {
    /**
     * No description
     *
     * @tags Seller
     * @name RegisterSellerSellerSignupPost
     * @summary Register Seller
     * @request POST:/seller/signup
     */
    registerSellerSellerSignupPost: (
      data: SellerCreate,
      params: RequestParams = {},
    ) =>
      this.request<SellerRead, HTTPValidationError>({
        path: `/seller/signup`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name LoginSellerSellerTokenPost
     * @summary Login Seller
     * @request POST:/seller/token
     */
    loginSellerSellerTokenPost: (
      data: BodyLoginSellerSellerTokenPost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/token`,
        method: "POST",
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name VerifySellerEmailSellerVerifyGet
     * @summary Verify Seller Email
     * @request GET:/seller/verify
     */
    verifySellerEmailSellerVerifyGet: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/verify`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name ForgotPasswordSellerForgotPasswordGet
     * @summary Forgot Password
     * @request GET:/seller/forgot-password
     */
    forgotPasswordSellerForgotPasswordGet: (
      query: {
        /**
         * Email
         * @format email
         */
        email: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/forgot-password`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name ResetPasswordFormSellerResetPasswordFormGet
     * @summary Reset Password Form
     * @request GET:/seller/reset-password-form
     */
    resetPasswordFormSellerResetPasswordFormGet: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/reset-password-form`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name ResetPasswordSellerResetPasswordPost
     * @summary Reset Password
     * @request POST:/seller/reset-password
     */
    resetPasswordSellerResetPasswordPost: (
      query: {
        /** Token */
        token: string;
      },
      data: BodyResetPasswordSellerResetPasswordPost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/reset-password`,
        method: "POST",
        query: query,
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name LogoutSellerSellerLogoutGet
     * @summary Logout Seller
     * @request GET:/seller/logout
     * @secure
     */
    logoutSellerSellerLogoutGet: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/seller/logout`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),
  };
  partner = {
    /**
     * No description
     *
     * @tags Delivery Partner
     * @name RegisterDeliveryPartnerPartnerSignupPost
     * @summary Register Delivery Partner
     * @request POST:/partner/signup
     */
    registerDeliveryPartnerPartnerSignupPost: (
      data: DeliveryPartnerCreate,
      params: RequestParams = {},
    ) =>
      this.request<DeliveryPartnerRead, HTTPValidationError>({
        path: `/partner/signup`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name LoginDeliveryPartnerPartnerTokenPost
     * @summary Login Delivery Partner
     * @request POST:/partner/token
     */
    loginDeliveryPartnerPartnerTokenPost: (
      data: BodyLoginDeliveryPartnerPartnerTokenPost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partner/token`,
        method: "POST",
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name VerifyDeliveryPartnerEmailPartnerVerifyGet
     * @summary Verify Delivery Partner Email
     * @request GET:/partner/verify
     */
    verifyDeliveryPartnerEmailPartnerVerifyGet: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partner/verify`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name UpdateDeliveryPartnerPartnerPost
     * @summary Update Delivery Partner
     * @request POST:/partner/
     * @secure
     */
    updateDeliveryPartnerPartnerPost: (
      data: DeliveryPartnerUpdate,
      params: RequestParams = {},
    ) =>
      this.request<DeliveryPartnerRead, HTTPValidationError>({
        path: `/partner/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name LogoutDeliveryPartnerPartnerLogoutGet
     * @summary Logout Delivery Partner
     * @request GET:/partner/logout
     * @secure
     */
    logoutDeliveryPartnerPartnerLogoutGet: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/partner/logout`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),
  };
}
