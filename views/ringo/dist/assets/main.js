var process = { env: { NODE_ENV: "production" } };
var _E = { exports: {} }, av = {}, RE = { exports: {} }, St = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var lR;
function uk() {
  if (lR) return St;
  lR = 1;
  var O = Symbol.for("react.element"), A = Symbol.for("react.portal"), T = Symbol.for("react.fragment"), oe = Symbol.for("react.strict_mode"), ke = Symbol.for("react.profiler"), He = Symbol.for("react.provider"), S = Symbol.for("react.context"), ft = Symbol.for("react.forward_ref"), ee = Symbol.for("react.suspense"), ne = Symbol.for("react.memo"), Ve = Symbol.for("react.lazy"), te = Symbol.iterator;
  function me(k) {
    return k === null || typeof k != "object" ? null : (k = te && k[te] || k["@@iterator"], typeof k == "function" ? k : null);
  }
  var fe = { isMounted: function() {
    return !1;
  }, enqueueForceUpdate: function() {
  }, enqueueReplaceState: function() {
  }, enqueueSetState: function() {
  } }, qe = Object.assign, Et = {};
  function mt(k, B, $e) {
    this.props = k, this.context = B, this.refs = Et, this.updater = $e || fe;
  }
  mt.prototype.isReactComponent = {}, mt.prototype.setState = function(k, B) {
    if (typeof k != "object" && typeof k != "function" && k != null) throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
    this.updater.enqueueSetState(this, k, B, "setState");
  }, mt.prototype.forceUpdate = function(k) {
    this.updater.enqueueForceUpdate(this, k, "forceUpdate");
  };
  function dn() {
  }
  dn.prototype = mt.prototype;
  function ht(k, B, $e) {
    this.props = k, this.context = B, this.refs = Et, this.updater = $e || fe;
  }
  var Ke = ht.prototype = new dn();
  Ke.constructor = ht, qe(Ke, mt.prototype), Ke.isPureReactComponent = !0;
  var yt = Array.isArray, De = Object.prototype.hasOwnProperty, dt = { current: null }, Be = { key: !0, ref: !0, __self: !0, __source: !0 };
  function ln(k, B, $e) {
    var Fe, ut = {}, rt = null, tt = null;
    if (B != null) for (Fe in B.ref !== void 0 && (tt = B.ref), B.key !== void 0 && (rt = "" + B.key), B) De.call(B, Fe) && !Be.hasOwnProperty(Fe) && (ut[Fe] = B[Fe]);
    var at = arguments.length - 2;
    if (at === 1) ut.children = $e;
    else if (1 < at) {
      for (var ot = Array(at), $t = 0; $t < at; $t++) ot[$t] = arguments[$t + 2];
      ut.children = ot;
    }
    if (k && k.defaultProps) for (Fe in at = k.defaultProps, at) ut[Fe] === void 0 && (ut[Fe] = at[Fe]);
    return { $$typeof: O, type: k, key: rt, ref: tt, props: ut, _owner: dt.current };
  }
  function Vt(k, B) {
    return { $$typeof: O, type: k.type, key: B, ref: k.ref, props: k.props, _owner: k._owner };
  }
  function Jt(k) {
    return typeof k == "object" && k !== null && k.$$typeof === O;
  }
  function un(k) {
    var B = { "=": "=0", ":": "=2" };
    return "$" + k.replace(/[=:]/g, function($e) {
      return B[$e];
    });
  }
  var kt = /\/+/g;
  function Le(k, B) {
    return typeof k == "object" && k !== null && k.key != null ? un("" + k.key) : B.toString(36);
  }
  function Ft(k, B, $e, Fe, ut) {
    var rt = typeof k;
    (rt === "undefined" || rt === "boolean") && (k = null);
    var tt = !1;
    if (k === null) tt = !0;
    else switch (rt) {
      case "string":
      case "number":
        tt = !0;
        break;
      case "object":
        switch (k.$$typeof) {
          case O:
          case A:
            tt = !0;
        }
    }
    if (tt) return tt = k, ut = ut(tt), k = Fe === "" ? "." + Le(tt, 0) : Fe, yt(ut) ? ($e = "", k != null && ($e = k.replace(kt, "$&/") + "/"), Ft(ut, B, $e, "", function($t) {
      return $t;
    })) : ut != null && (Jt(ut) && (ut = Vt(ut, $e + (!ut.key || tt && tt.key === ut.key ? "" : ("" + ut.key).replace(kt, "$&/") + "/") + k)), B.push(ut)), 1;
    if (tt = 0, Fe = Fe === "" ? "." : Fe + ":", yt(k)) for (var at = 0; at < k.length; at++) {
      rt = k[at];
      var ot = Fe + Le(rt, at);
      tt += Ft(rt, B, $e, ot, ut);
    }
    else if (ot = me(k), typeof ot == "function") for (k = ot.call(k), at = 0; !(rt = k.next()).done; ) rt = rt.value, ot = Fe + Le(rt, at++), tt += Ft(rt, B, $e, ot, ut);
    else if (rt === "object") throw B = String(k), Error("Objects are not valid as a React child (found: " + (B === "[object Object]" ? "object with keys {" + Object.keys(k).join(", ") + "}" : B) + "). If you meant to render a collection of children, use an array instead.");
    return tt;
  }
  function Dt(k, B, $e) {
    if (k == null) return k;
    var Fe = [], ut = 0;
    return Ft(k, Fe, "", "", function(rt) {
      return B.call($e, rt, ut++);
    }), Fe;
  }
  function Nt(k) {
    if (k._status === -1) {
      var B = k._result;
      B = B(), B.then(function($e) {
        (k._status === 0 || k._status === -1) && (k._status = 1, k._result = $e);
      }, function($e) {
        (k._status === 0 || k._status === -1) && (k._status = 2, k._result = $e);
      }), k._status === -1 && (k._status = 0, k._result = B);
    }
    if (k._status === 1) return k._result.default;
    throw k._result;
  }
  var Re = { current: null }, J = { transition: null }, Te = { ReactCurrentDispatcher: Re, ReactCurrentBatchConfig: J, ReactCurrentOwner: dt };
  function ie() {
    throw Error("act(...) is not supported in production builds of React.");
  }
  return St.Children = { map: Dt, forEach: function(k, B, $e) {
    Dt(k, function() {
      B.apply(this, arguments);
    }, $e);
  }, count: function(k) {
    var B = 0;
    return Dt(k, function() {
      B++;
    }), B;
  }, toArray: function(k) {
    return Dt(k, function(B) {
      return B;
    }) || [];
  }, only: function(k) {
    if (!Jt(k)) throw Error("React.Children.only expected to receive a single React element child.");
    return k;
  } }, St.Component = mt, St.Fragment = T, St.Profiler = ke, St.PureComponent = ht, St.StrictMode = oe, St.Suspense = ee, St.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Te, St.act = ie, St.cloneElement = function(k, B, $e) {
    if (k == null) throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + k + ".");
    var Fe = qe({}, k.props), ut = k.key, rt = k.ref, tt = k._owner;
    if (B != null) {
      if (B.ref !== void 0 && (rt = B.ref, tt = dt.current), B.key !== void 0 && (ut = "" + B.key), k.type && k.type.defaultProps) var at = k.type.defaultProps;
      for (ot in B) De.call(B, ot) && !Be.hasOwnProperty(ot) && (Fe[ot] = B[ot] === void 0 && at !== void 0 ? at[ot] : B[ot]);
    }
    var ot = arguments.length - 2;
    if (ot === 1) Fe.children = $e;
    else if (1 < ot) {
      at = Array(ot);
      for (var $t = 0; $t < ot; $t++) at[$t] = arguments[$t + 2];
      Fe.children = at;
    }
    return { $$typeof: O, type: k.type, key: ut, ref: rt, props: Fe, _owner: tt };
  }, St.createContext = function(k) {
    return k = { $$typeof: S, _currentValue: k, _currentValue2: k, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, k.Provider = { $$typeof: He, _context: k }, k.Consumer = k;
  }, St.createElement = ln, St.createFactory = function(k) {
    var B = ln.bind(null, k);
    return B.type = k, B;
  }, St.createRef = function() {
    return { current: null };
  }, St.forwardRef = function(k) {
    return { $$typeof: ft, render: k };
  }, St.isValidElement = Jt, St.lazy = function(k) {
    return { $$typeof: Ve, _payload: { _status: -1, _result: k }, _init: Nt };
  }, St.memo = function(k, B) {
    return { $$typeof: ne, type: k, compare: B === void 0 ? null : B };
  }, St.startTransition = function(k) {
    var B = J.transition;
    J.transition = {};
    try {
      k();
    } finally {
      J.transition = B;
    }
  }, St.unstable_act = ie, St.useCallback = function(k, B) {
    return Re.current.useCallback(k, B);
  }, St.useContext = function(k) {
    return Re.current.useContext(k);
  }, St.useDebugValue = function() {
  }, St.useDeferredValue = function(k) {
    return Re.current.useDeferredValue(k);
  }, St.useEffect = function(k, B) {
    return Re.current.useEffect(k, B);
  }, St.useId = function() {
    return Re.current.useId();
  }, St.useImperativeHandle = function(k, B, $e) {
    return Re.current.useImperativeHandle(k, B, $e);
  }, St.useInsertionEffect = function(k, B) {
    return Re.current.useInsertionEffect(k, B);
  }, St.useLayoutEffect = function(k, B) {
    return Re.current.useLayoutEffect(k, B);
  }, St.useMemo = function(k, B) {
    return Re.current.useMemo(k, B);
  }, St.useReducer = function(k, B, $e) {
    return Re.current.useReducer(k, B, $e);
  }, St.useRef = function(k) {
    return Re.current.useRef(k);
  }, St.useState = function(k) {
    return Re.current.useState(k);
  }, St.useSyncExternalStore = function(k, B, $e) {
    return Re.current.useSyncExternalStore(k, B, $e);
  }, St.useTransition = function() {
    return Re.current.useTransition();
  }, St.version = "18.3.1", St;
}
var uv = { exports: {} };
/**
 * @license React
 * react.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
uv.exports;
var uR;
function ok() {
  return uR || (uR = 1, function(O, A) {
    process.env.NODE_ENV !== "production" && function() {
      typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(new Error());
      var T = "18.3.1", oe = Symbol.for("react.element"), ke = Symbol.for("react.portal"), He = Symbol.for("react.fragment"), S = Symbol.for("react.strict_mode"), ft = Symbol.for("react.profiler"), ee = Symbol.for("react.provider"), ne = Symbol.for("react.context"), Ve = Symbol.for("react.forward_ref"), te = Symbol.for("react.suspense"), me = Symbol.for("react.suspense_list"), fe = Symbol.for("react.memo"), qe = Symbol.for("react.lazy"), Et = Symbol.for("react.offscreen"), mt = Symbol.iterator, dn = "@@iterator";
      function ht(h) {
        if (h === null || typeof h != "object")
          return null;
        var C = mt && h[mt] || h[dn];
        return typeof C == "function" ? C : null;
      }
      var Ke = {
        /**
         * @internal
         * @type {ReactComponent}
         */
        current: null
      }, yt = {
        transition: null
      }, De = {
        current: null,
        // Used to reproduce behavior of `batchedUpdates` in legacy mode.
        isBatchingLegacy: !1,
        didScheduleLegacyUpdate: !1
      }, dt = {
        /**
         * @internal
         * @type {ReactComponent}
         */
        current: null
      }, Be = {}, ln = null;
      function Vt(h) {
        ln = h;
      }
      Be.setExtraStackFrame = function(h) {
        ln = h;
      }, Be.getCurrentStack = null, Be.getStackAddendum = function() {
        var h = "";
        ln && (h += ln);
        var C = Be.getCurrentStack;
        return C && (h += C() || ""), h;
      };
      var Jt = !1, un = !1, kt = !1, Le = !1, Ft = !1, Dt = {
        ReactCurrentDispatcher: Ke,
        ReactCurrentBatchConfig: yt,
        ReactCurrentOwner: dt
      };
      Dt.ReactDebugCurrentFrame = Be, Dt.ReactCurrentActQueue = De;
      function Nt(h) {
        {
          for (var C = arguments.length, z = new Array(C > 1 ? C - 1 : 0), H = 1; H < C; H++)
            z[H - 1] = arguments[H];
          J("warn", h, z);
        }
      }
      function Re(h) {
        {
          for (var C = arguments.length, z = new Array(C > 1 ? C - 1 : 0), H = 1; H < C; H++)
            z[H - 1] = arguments[H];
          J("error", h, z);
        }
      }
      function J(h, C, z) {
        {
          var H = Dt.ReactDebugCurrentFrame, Z = H.getStackAddendum();
          Z !== "" && (C += "%s", z = z.concat([Z]));
          var Me = z.map(function(le) {
            return String(le);
          });
          Me.unshift("Warning: " + C), Function.prototype.apply.call(console[h], console, Me);
        }
      }
      var Te = {};
      function ie(h, C) {
        {
          var z = h.constructor, H = z && (z.displayName || z.name) || "ReactClass", Z = H + "." + C;
          if (Te[Z])
            return;
          Re("Can't call %s on a component that is not yet mounted. This is a no-op, but it might indicate a bug in your application. Instead, assign to `this.state` directly or define a `state = {};` class property with the desired state in the %s component.", C, H), Te[Z] = !0;
        }
      }
      var k = {
        /**
         * Checks whether or not this composite component is mounted.
         * @param {ReactClass} publicInstance The instance we want to test.
         * @return {boolean} True if mounted, false otherwise.
         * @protected
         * @final
         */
        isMounted: function(h) {
          return !1;
        },
        /**
         * Forces an update. This should only be invoked when it is known with
         * certainty that we are **not** in a DOM transaction.
         *
         * You may want to call this when you know that some deeper aspect of the
         * component's state has changed but `setState` was not called.
         *
         * This will not invoke `shouldComponentUpdate`, but it will invoke
         * `componentWillUpdate` and `componentDidUpdate`.
         *
         * @param {ReactClass} publicInstance The instance that should rerender.
         * @param {?function} callback Called after component is updated.
         * @param {?string} callerName name of the calling function in the public API.
         * @internal
         */
        enqueueForceUpdate: function(h, C, z) {
          ie(h, "forceUpdate");
        },
        /**
         * Replaces all of the state. Always use this or `setState` to mutate state.
         * You should treat `this.state` as immutable.
         *
         * There is no guarantee that `this.state` will be immediately updated, so
         * accessing `this.state` after calling this method may return the old value.
         *
         * @param {ReactClass} publicInstance The instance that should rerender.
         * @param {object} completeState Next state.
         * @param {?function} callback Called after component is updated.
         * @param {?string} callerName name of the calling function in the public API.
         * @internal
         */
        enqueueReplaceState: function(h, C, z, H) {
          ie(h, "replaceState");
        },
        /**
         * Sets a subset of the state. This only exists because _pendingState is
         * internal. This provides a merging strategy that is not available to deep
         * properties which is confusing. TODO: Expose pendingState or don't use it
         * during the merge.
         *
         * @param {ReactClass} publicInstance The instance that should rerender.
         * @param {object} partialState Next partial state to be merged with state.
         * @param {?function} callback Called after component is updated.
         * @param {?string} Name of the calling function in the public API.
         * @internal
         */
        enqueueSetState: function(h, C, z, H) {
          ie(h, "setState");
        }
      }, B = Object.assign, $e = {};
      Object.freeze($e);
      function Fe(h, C, z) {
        this.props = h, this.context = C, this.refs = $e, this.updater = z || k;
      }
      Fe.prototype.isReactComponent = {}, Fe.prototype.setState = function(h, C) {
        if (typeof h != "object" && typeof h != "function" && h != null)
          throw new Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
        this.updater.enqueueSetState(this, h, C, "setState");
      }, Fe.prototype.forceUpdate = function(h) {
        this.updater.enqueueForceUpdate(this, h, "forceUpdate");
      };
      {
        var ut = {
          isMounted: ["isMounted", "Instead, make sure to clean up subscriptions and pending requests in componentWillUnmount to prevent memory leaks."],
          replaceState: ["replaceState", "Refactor your code to use setState instead (see https://github.com/facebook/react/issues/3236)."]
        }, rt = function(h, C) {
          Object.defineProperty(Fe.prototype, h, {
            get: function() {
              Nt("%s(...) is deprecated in plain JavaScript React classes. %s", C[0], C[1]);
            }
          });
        };
        for (var tt in ut)
          ut.hasOwnProperty(tt) && rt(tt, ut[tt]);
      }
      function at() {
      }
      at.prototype = Fe.prototype;
      function ot(h, C, z) {
        this.props = h, this.context = C, this.refs = $e, this.updater = z || k;
      }
      var $t = ot.prototype = new at();
      $t.constructor = ot, B($t, Fe.prototype), $t.isPureReactComponent = !0;
      function Nn() {
        var h = {
          current: null
        };
        return Object.seal(h), h;
      }
      var xr = Array.isArray;
      function _n(h) {
        return xr(h);
      }
      function ar(h) {
        {
          var C = typeof Symbol == "function" && Symbol.toStringTag, z = C && h[Symbol.toStringTag] || h.constructor.name || "Object";
          return z;
        }
      }
      function $n(h) {
        try {
          return In(h), !1;
        } catch {
          return !0;
        }
      }
      function In(h) {
        return "" + h;
      }
      function Wr(h) {
        if ($n(h))
          return Re("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", ar(h)), In(h);
      }
      function vi(h, C, z) {
        var H = h.displayName;
        if (H)
          return H;
        var Z = C.displayName || C.name || "";
        return Z !== "" ? z + "(" + Z + ")" : z;
      }
      function fa(h) {
        return h.displayName || "Context";
      }
      function Xn(h) {
        if (h == null)
          return null;
        if (typeof h.tag == "number" && Re("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof h == "function")
          return h.displayName || h.name || null;
        if (typeof h == "string")
          return h;
        switch (h) {
          case He:
            return "Fragment";
          case ke:
            return "Portal";
          case ft:
            return "Profiler";
          case S:
            return "StrictMode";
          case te:
            return "Suspense";
          case me:
            return "SuspenseList";
        }
        if (typeof h == "object")
          switch (h.$$typeof) {
            case ne:
              var C = h;
              return fa(C) + ".Consumer";
            case ee:
              var z = h;
              return fa(z._context) + ".Provider";
            case Ve:
              return vi(h, h.render, "ForwardRef");
            case fe:
              var H = h.displayName || null;
              return H !== null ? H : Xn(h.type) || "Memo";
            case qe: {
              var Z = h, Me = Z._payload, le = Z._init;
              try {
                return Xn(le(Me));
              } catch {
                return null;
              }
            }
          }
        return null;
      }
      var Rn = Object.prototype.hasOwnProperty, Yn = {
        key: !0,
        ref: !0,
        __self: !0,
        __source: !0
      }, Er, qa, Ln;
      Ln = {};
      function Cr(h) {
        if (Rn.call(h, "ref")) {
          var C = Object.getOwnPropertyDescriptor(h, "ref").get;
          if (C && C.isReactWarning)
            return !1;
        }
        return h.ref !== void 0;
      }
      function da(h) {
        if (Rn.call(h, "key")) {
          var C = Object.getOwnPropertyDescriptor(h, "key").get;
          if (C && C.isReactWarning)
            return !1;
        }
        return h.key !== void 0;
      }
      function Ka(h, C) {
        var z = function() {
          Er || (Er = !0, Re("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", C));
        };
        z.isReactWarning = !0, Object.defineProperty(h, "key", {
          get: z,
          configurable: !0
        });
      }
      function hi(h, C) {
        var z = function() {
          qa || (qa = !0, Re("%s: `ref` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", C));
        };
        z.isReactWarning = !0, Object.defineProperty(h, "ref", {
          get: z,
          configurable: !0
        });
      }
      function re(h) {
        if (typeof h.ref == "string" && dt.current && h.__self && dt.current.stateNode !== h.__self) {
          var C = Xn(dt.current.type);
          Ln[C] || (Re('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. This case cannot be automatically converted to an arrow function. We ask you to manually fix this case by using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', C, h.ref), Ln[C] = !0);
        }
      }
      var be = function(h, C, z, H, Z, Me, le) {
        var Ae = {
          // This tag allows us to uniquely identify this as a React Element
          $$typeof: oe,
          // Built-in properties that belong on the element
          type: h,
          key: C,
          ref: z,
          props: le,
          // Record the component responsible for creating this element.
          _owner: Me
        };
        return Ae._store = {}, Object.defineProperty(Ae._store, "validated", {
          configurable: !1,
          enumerable: !1,
          writable: !0,
          value: !1
        }), Object.defineProperty(Ae, "_self", {
          configurable: !1,
          enumerable: !1,
          writable: !1,
          value: H
        }), Object.defineProperty(Ae, "_source", {
          configurable: !1,
          enumerable: !1,
          writable: !1,
          value: Z
        }), Object.freeze && (Object.freeze(Ae.props), Object.freeze(Ae)), Ae;
      };
      function it(h, C, z) {
        var H, Z = {}, Me = null, le = null, Ae = null, vt = null;
        if (C != null) {
          Cr(C) && (le = C.ref, re(C)), da(C) && (Wr(C.key), Me = "" + C.key), Ae = C.__self === void 0 ? null : C.__self, vt = C.__source === void 0 ? null : C.__source;
          for (H in C)
            Rn.call(C, H) && !Yn.hasOwnProperty(H) && (Z[H] = C[H]);
        }
        var xt = arguments.length - 2;
        if (xt === 1)
          Z.children = z;
        else if (xt > 1) {
          for (var rn = Array(xt), Wt = 0; Wt < xt; Wt++)
            rn[Wt] = arguments[Wt + 2];
          Object.freeze && Object.freeze(rn), Z.children = rn;
        }
        if (h && h.defaultProps) {
          var lt = h.defaultProps;
          for (H in lt)
            Z[H] === void 0 && (Z[H] = lt[H]);
        }
        if (Me || le) {
          var Gt = typeof h == "function" ? h.displayName || h.name || "Unknown" : h;
          Me && Ka(Z, Gt), le && hi(Z, Gt);
        }
        return be(h, Me, le, Ae, vt, dt.current, Z);
      }
      function Ht(h, C) {
        var z = be(h.type, C, h.ref, h._self, h._source, h._owner, h.props);
        return z;
      }
      function en(h, C, z) {
        if (h == null)
          throw new Error("React.cloneElement(...): The argument must be a React element, but you passed " + h + ".");
        var H, Z = B({}, h.props), Me = h.key, le = h.ref, Ae = h._self, vt = h._source, xt = h._owner;
        if (C != null) {
          Cr(C) && (le = C.ref, xt = dt.current), da(C) && (Wr(C.key), Me = "" + C.key);
          var rn;
          h.type && h.type.defaultProps && (rn = h.type.defaultProps);
          for (H in C)
            Rn.call(C, H) && !Yn.hasOwnProperty(H) && (C[H] === void 0 && rn !== void 0 ? Z[H] = rn[H] : Z[H] = C[H]);
        }
        var Wt = arguments.length - 2;
        if (Wt === 1)
          Z.children = z;
        else if (Wt > 1) {
          for (var lt = Array(Wt), Gt = 0; Gt < Wt; Gt++)
            lt[Gt] = arguments[Gt + 2];
          Z.children = lt;
        }
        return be(h.type, Me, le, Ae, vt, xt, Z);
      }
      function hn(h) {
        return typeof h == "object" && h !== null && h.$$typeof === oe;
      }
      var on = ".", Zn = ":";
      function tn(h) {
        var C = /[=:]/g, z = {
          "=": "=0",
          ":": "=2"
        }, H = h.replace(C, function(Z) {
          return z[Z];
        });
        return "$" + H;
      }
      var It = !1, Yt = /\/+/g;
      function pa(h) {
        return h.replace(Yt, "$&/");
      }
      function _r(h, C) {
        return typeof h == "object" && h !== null && h.key != null ? (Wr(h.key), tn("" + h.key)) : C.toString(36);
      }
      function xa(h, C, z, H, Z) {
        var Me = typeof h;
        (Me === "undefined" || Me === "boolean") && (h = null);
        var le = !1;
        if (h === null)
          le = !0;
        else
          switch (Me) {
            case "string":
            case "number":
              le = !0;
              break;
            case "object":
              switch (h.$$typeof) {
                case oe:
                case ke:
                  le = !0;
              }
          }
        if (le) {
          var Ae = h, vt = Z(Ae), xt = H === "" ? on + _r(Ae, 0) : H;
          if (_n(vt)) {
            var rn = "";
            xt != null && (rn = pa(xt) + "/"), xa(vt, C, rn, "", function(nd) {
              return nd;
            });
          } else vt != null && (hn(vt) && (vt.key && (!Ae || Ae.key !== vt.key) && Wr(vt.key), vt = Ht(
            vt,
            // Keep both the (mapped) and old keys if they differ, just as
            // traverseAllChildren used to do for objects as children
            z + // $FlowFixMe Flow incorrectly thinks React.Portal doesn't have a key
            (vt.key && (!Ae || Ae.key !== vt.key) ? (
              // $FlowFixMe Flow incorrectly thinks existing element's key can be a number
              // eslint-disable-next-line react-internal/safe-string-coercion
              pa("" + vt.key) + "/"
            ) : "") + xt
          )), C.push(vt));
          return 1;
        }
        var Wt, lt, Gt = 0, mn = H === "" ? on : H + Zn;
        if (_n(h))
          for (var Dl = 0; Dl < h.length; Dl++)
            Wt = h[Dl], lt = mn + _r(Wt, Dl), Gt += xa(Wt, C, z, lt, Z);
        else {
          var ns = ht(h);
          if (typeof ns == "function") {
            var Qi = h;
            ns === Qi.entries && (It || Nt("Using Maps as children is not supported. Use an array of keyed ReactElements instead."), It = !0);
            for (var rs = ns.call(Qi), hu, td = 0; !(hu = rs.next()).done; )
              Wt = hu.value, lt = mn + _r(Wt, td++), Gt += xa(Wt, C, z, lt, Z);
          } else if (Me === "object") {
            var hc = String(h);
            throw new Error("Objects are not valid as a React child (found: " + (hc === "[object Object]" ? "object with keys {" + Object.keys(h).join(", ") + "}" : hc) + "). If you meant to render a collection of children, use an array instead.");
          }
        }
        return Gt;
      }
      function $i(h, C, z) {
        if (h == null)
          return h;
        var H = [], Z = 0;
        return xa(h, H, "", "", function(Me) {
          return C.call(z, Me, Z++);
        }), H;
      }
      function lu(h) {
        var C = 0;
        return $i(h, function() {
          C++;
        }), C;
      }
      function uu(h, C, z) {
        $i(h, function() {
          C.apply(this, arguments);
        }, z);
      }
      function El(h) {
        return $i(h, function(C) {
          return C;
        }) || [];
      }
      function Cl(h) {
        if (!hn(h))
          throw new Error("React.Children.only expected to receive a single React element child.");
        return h;
      }
      function ou(h) {
        var C = {
          $$typeof: ne,
          // As a workaround to support multiple concurrent renderers, we categorize
          // some renderers as primary and others as secondary. We only expect
          // there to be two concurrent renderers at most: React Native (primary) and
          // Fabric (secondary); React DOM (primary) and React ART (secondary).
          // Secondary renderers store their context values on separate fields.
          _currentValue: h,
          _currentValue2: h,
          // Used to track how many concurrent renderers this context currently
          // supports within in a single renderer. Such as parallel server rendering.
          _threadCount: 0,
          // These are circular
          Provider: null,
          Consumer: null,
          // Add these to use same hidden class in VM as ServerContext
          _defaultValue: null,
          _globalName: null
        };
        C.Provider = {
          $$typeof: ee,
          _context: C
        };
        var z = !1, H = !1, Z = !1;
        {
          var Me = {
            $$typeof: ne,
            _context: C
          };
          Object.defineProperties(Me, {
            Provider: {
              get: function() {
                return H || (H = !0, Re("Rendering <Context.Consumer.Provider> is not supported and will be removed in a future major release. Did you mean to render <Context.Provider> instead?")), C.Provider;
              },
              set: function(le) {
                C.Provider = le;
              }
            },
            _currentValue: {
              get: function() {
                return C._currentValue;
              },
              set: function(le) {
                C._currentValue = le;
              }
            },
            _currentValue2: {
              get: function() {
                return C._currentValue2;
              },
              set: function(le) {
                C._currentValue2 = le;
              }
            },
            _threadCount: {
              get: function() {
                return C._threadCount;
              },
              set: function(le) {
                C._threadCount = le;
              }
            },
            Consumer: {
              get: function() {
                return z || (z = !0, Re("Rendering <Context.Consumer.Consumer> is not supported and will be removed in a future major release. Did you mean to render <Context.Consumer> instead?")), C.Consumer;
              }
            },
            displayName: {
              get: function() {
                return C.displayName;
              },
              set: function(le) {
                Z || (Nt("Setting `displayName` on Context.Consumer has no effect. You should set it directly on the context with Context.displayName = '%s'.", le), Z = !0);
              }
            }
          }), C.Consumer = Me;
        }
        return C._currentRenderer = null, C._currentRenderer2 = null, C;
      }
      var kr = -1, Dr = 0, ir = 1, mi = 2;
      function Xa(h) {
        if (h._status === kr) {
          var C = h._result, z = C();
          if (z.then(function(Me) {
            if (h._status === Dr || h._status === kr) {
              var le = h;
              le._status = ir, le._result = Me;
            }
          }, function(Me) {
            if (h._status === Dr || h._status === kr) {
              var le = h;
              le._status = mi, le._result = Me;
            }
          }), h._status === kr) {
            var H = h;
            H._status = Dr, H._result = z;
          }
        }
        if (h._status === ir) {
          var Z = h._result;
          return Z === void 0 && Re(`lazy: Expected the result of a dynamic import() call. Instead received: %s

Your code should look like: 
  const MyComponent = lazy(() => import('./MyComponent'))

Did you accidentally put curly braces around the import?`, Z), "default" in Z || Re(`lazy: Expected the result of a dynamic import() call. Instead received: %s

Your code should look like: 
  const MyComponent = lazy(() => import('./MyComponent'))`, Z), Z.default;
        } else
          throw h._result;
      }
      function yi(h) {
        var C = {
          // We use these fields to store the result.
          _status: kr,
          _result: h
        }, z = {
          $$typeof: qe,
          _payload: C,
          _init: Xa
        };
        {
          var H, Z;
          Object.defineProperties(z, {
            defaultProps: {
              configurable: !0,
              get: function() {
                return H;
              },
              set: function(Me) {
                Re("React.lazy(...): It is not supported to assign `defaultProps` to a lazy component import. Either specify them where the component is defined, or create a wrapping component around it."), H = Me, Object.defineProperty(z, "defaultProps", {
                  enumerable: !0
                });
              }
            },
            propTypes: {
              configurable: !0,
              get: function() {
                return Z;
              },
              set: function(Me) {
                Re("React.lazy(...): It is not supported to assign `propTypes` to a lazy component import. Either specify them where the component is defined, or create a wrapping component around it."), Z = Me, Object.defineProperty(z, "propTypes", {
                  enumerable: !0
                });
              }
            }
          });
        }
        return z;
      }
      function gi(h) {
        h != null && h.$$typeof === fe ? Re("forwardRef requires a render function but received a `memo` component. Instead of forwardRef(memo(...)), use memo(forwardRef(...)).") : typeof h != "function" ? Re("forwardRef requires a render function but was given %s.", h === null ? "null" : typeof h) : h.length !== 0 && h.length !== 2 && Re("forwardRef render functions accept exactly two parameters: props and ref. %s", h.length === 1 ? "Did you forget to use the ref parameter?" : "Any additional parameter will be undefined."), h != null && (h.defaultProps != null || h.propTypes != null) && Re("forwardRef render functions do not support propTypes or defaultProps. Did you accidentally pass a React component?");
        var C = {
          $$typeof: Ve,
          render: h
        };
        {
          var z;
          Object.defineProperty(C, "displayName", {
            enumerable: !1,
            configurable: !0,
            get: function() {
              return z;
            },
            set: function(H) {
              z = H, !h.name && !h.displayName && (h.displayName = H);
            }
          });
        }
        return C;
      }
      var _;
      _ = Symbol.for("react.module.reference");
      function I(h) {
        return !!(typeof h == "string" || typeof h == "function" || h === He || h === ft || Ft || h === S || h === te || h === me || Le || h === Et || Jt || un || kt || typeof h == "object" && h !== null && (h.$$typeof === qe || h.$$typeof === fe || h.$$typeof === ee || h.$$typeof === ne || h.$$typeof === Ve || // This needs to include all possible module reference object
        // types supported by any Flight configuration anywhere since
        // we don't know which Flight build this will end up being used
        // with.
        h.$$typeof === _ || h.getModuleId !== void 0));
      }
      function ue(h, C) {
        I(h) || Re("memo: The first argument must be a component. Instead received: %s", h === null ? "null" : typeof h);
        var z = {
          $$typeof: fe,
          type: h,
          compare: C === void 0 ? null : C
        };
        {
          var H;
          Object.defineProperty(z, "displayName", {
            enumerable: !1,
            configurable: !0,
            get: function() {
              return H;
            },
            set: function(Z) {
              H = Z, !h.name && !h.displayName && (h.displayName = Z);
            }
          });
        }
        return z;
      }
      function ge() {
        var h = Ke.current;
        return h === null && Re(`Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://reactjs.org/link/invalid-hook-call for tips about how to debug and fix this problem.`), h;
      }
      function Ze(h) {
        var C = ge();
        if (h._context !== void 0) {
          var z = h._context;
          z.Consumer === h ? Re("Calling useContext(Context.Consumer) is not supported, may cause bugs, and will be removed in a future major release. Did you mean to call useContext(Context) instead?") : z.Provider === h && Re("Calling useContext(Context.Provider) is not supported. Did you mean to call useContext(Context) instead?");
        }
        return C.useContext(h);
      }
      function We(h) {
        var C = ge();
        return C.useState(h);
      }
      function pt(h, C, z) {
        var H = ge();
        return H.useReducer(h, C, z);
      }
      function st(h) {
        var C = ge();
        return C.useRef(h);
      }
      function Tn(h, C) {
        var z = ge();
        return z.useEffect(h, C);
      }
      function nn(h, C) {
        var z = ge();
        return z.useInsertionEffect(h, C);
      }
      function sn(h, C) {
        var z = ge();
        return z.useLayoutEffect(h, C);
      }
      function lr(h, C) {
        var z = ge();
        return z.useCallback(h, C);
      }
      function Za(h, C) {
        var z = ge();
        return z.useMemo(h, C);
      }
      function Ja(h, C, z) {
        var H = ge();
        return H.useImperativeHandle(h, C, z);
      }
      function Je(h, C) {
        {
          var z = ge();
          return z.useDebugValue(h, C);
        }
      }
      function nt() {
        var h = ge();
        return h.useTransition();
      }
      function ei(h) {
        var C = ge();
        return C.useDeferredValue(h);
      }
      function su() {
        var h = ge();
        return h.useId();
      }
      function cu(h, C, z) {
        var H = ge();
        return H.useSyncExternalStore(h, C, z);
      }
      var _l = 0, eo, Rl, Gr, Zo, Or, pc, vc;
      function to() {
      }
      to.__reactDisabledLog = !0;
      function Tl() {
        {
          if (_l === 0) {
            eo = console.log, Rl = console.info, Gr = console.warn, Zo = console.error, Or = console.group, pc = console.groupCollapsed, vc = console.groupEnd;
            var h = {
              configurable: !0,
              enumerable: !0,
              value: to,
              writable: !0
            };
            Object.defineProperties(console, {
              info: h,
              log: h,
              warn: h,
              error: h,
              group: h,
              groupCollapsed: h,
              groupEnd: h
            });
          }
          _l++;
        }
      }
      function va() {
        {
          if (_l--, _l === 0) {
            var h = {
              configurable: !0,
              enumerable: !0,
              writable: !0
            };
            Object.defineProperties(console, {
              log: B({}, h, {
                value: eo
              }),
              info: B({}, h, {
                value: Rl
              }),
              warn: B({}, h, {
                value: Gr
              }),
              error: B({}, h, {
                value: Zo
              }),
              group: B({}, h, {
                value: Or
              }),
              groupCollapsed: B({}, h, {
                value: pc
              }),
              groupEnd: B({}, h, {
                value: vc
              })
            });
          }
          _l < 0 && Re("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
        }
      }
      var ti = Dt.ReactCurrentDispatcher, ni;
      function no(h, C, z) {
        {
          if (ni === void 0)
            try {
              throw Error();
            } catch (Z) {
              var H = Z.stack.trim().match(/\n( *(at )?)/);
              ni = H && H[1] || "";
            }
          return `
` + ni + h;
        }
      }
      var fu = !1, bl;
      {
        var ro = typeof WeakMap == "function" ? WeakMap : Map;
        bl = new ro();
      }
      function ao(h, C) {
        if (!h || fu)
          return "";
        {
          var z = bl.get(h);
          if (z !== void 0)
            return z;
        }
        var H;
        fu = !0;
        var Z = Error.prepareStackTrace;
        Error.prepareStackTrace = void 0;
        var Me;
        Me = ti.current, ti.current = null, Tl();
        try {
          if (C) {
            var le = function() {
              throw Error();
            };
            if (Object.defineProperty(le.prototype, "props", {
              set: function() {
                throw Error();
              }
            }), typeof Reflect == "object" && Reflect.construct) {
              try {
                Reflect.construct(le, []);
              } catch (mn) {
                H = mn;
              }
              Reflect.construct(h, [], le);
            } else {
              try {
                le.call();
              } catch (mn) {
                H = mn;
              }
              h.call(le.prototype);
            }
          } else {
            try {
              throw Error();
            } catch (mn) {
              H = mn;
            }
            h();
          }
        } catch (mn) {
          if (mn && H && typeof mn.stack == "string") {
            for (var Ae = mn.stack.split(`
`), vt = H.stack.split(`
`), xt = Ae.length - 1, rn = vt.length - 1; xt >= 1 && rn >= 0 && Ae[xt] !== vt[rn]; )
              rn--;
            for (; xt >= 1 && rn >= 0; xt--, rn--)
              if (Ae[xt] !== vt[rn]) {
                if (xt !== 1 || rn !== 1)
                  do
                    if (xt--, rn--, rn < 0 || Ae[xt] !== vt[rn]) {
                      var Wt = `
` + Ae[xt].replace(" at new ", " at ");
                      return h.displayName && Wt.includes("<anonymous>") && (Wt = Wt.replace("<anonymous>", h.displayName)), typeof h == "function" && bl.set(h, Wt), Wt;
                    }
                  while (xt >= 1 && rn >= 0);
                break;
              }
          }
        } finally {
          fu = !1, ti.current = Me, va(), Error.prepareStackTrace = Z;
        }
        var lt = h ? h.displayName || h.name : "", Gt = lt ? no(lt) : "";
        return typeof h == "function" && bl.set(h, Gt), Gt;
      }
      function Ii(h, C, z) {
        return ao(h, !1);
      }
      function Jf(h) {
        var C = h.prototype;
        return !!(C && C.isReactComponent);
      }
      function Yi(h, C, z) {
        if (h == null)
          return "";
        if (typeof h == "function")
          return ao(h, Jf(h));
        if (typeof h == "string")
          return no(h);
        switch (h) {
          case te:
            return no("Suspense");
          case me:
            return no("SuspenseList");
        }
        if (typeof h == "object")
          switch (h.$$typeof) {
            case Ve:
              return Ii(h.render);
            case fe:
              return Yi(h.type, C, z);
            case qe: {
              var H = h, Z = H._payload, Me = H._init;
              try {
                return Yi(Me(Z), C, z);
              } catch {
              }
            }
          }
        return "";
      }
      var Lt = {}, io = Dt.ReactDebugCurrentFrame;
      function wt(h) {
        if (h) {
          var C = h._owner, z = Yi(h.type, h._source, C ? C.type : null);
          io.setExtraStackFrame(z);
        } else
          io.setExtraStackFrame(null);
      }
      function Jo(h, C, z, H, Z) {
        {
          var Me = Function.call.bind(Rn);
          for (var le in h)
            if (Me(h, le)) {
              var Ae = void 0;
              try {
                if (typeof h[le] != "function") {
                  var vt = Error((H || "React class") + ": " + z + " type `" + le + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof h[le] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                  throw vt.name = "Invariant Violation", vt;
                }
                Ae = h[le](C, le, H, z, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
              } catch (xt) {
                Ae = xt;
              }
              Ae && !(Ae instanceof Error) && (wt(Z), Re("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", H || "React class", z, le, typeof Ae), wt(null)), Ae instanceof Error && !(Ae.message in Lt) && (Lt[Ae.message] = !0, wt(Z), Re("Failed %s type: %s", z, Ae.message), wt(null));
            }
        }
      }
      function Si(h) {
        if (h) {
          var C = h._owner, z = Yi(h.type, h._source, C ? C.type : null);
          Vt(z);
        } else
          Vt(null);
      }
      var Qe;
      Qe = !1;
      function lo() {
        if (dt.current) {
          var h = Xn(dt.current.type);
          if (h)
            return `

Check the render method of \`` + h + "`.";
        }
        return "";
      }
      function ur(h) {
        if (h !== void 0) {
          var C = h.fileName.replace(/^.*[\\\/]/, ""), z = h.lineNumber;
          return `

Check your code at ` + C + ":" + z + ".";
        }
        return "";
      }
      function Ei(h) {
        return h != null ? ur(h.__source) : "";
      }
      var Nr = {};
      function Ci(h) {
        var C = lo();
        if (!C) {
          var z = typeof h == "string" ? h : h.displayName || h.name;
          z && (C = `

Check the top-level render call using <` + z + ">.");
        }
        return C;
      }
      function cn(h, C) {
        if (!(!h._store || h._store.validated || h.key != null)) {
          h._store.validated = !0;
          var z = Ci(C);
          if (!Nr[z]) {
            Nr[z] = !0;
            var H = "";
            h && h._owner && h._owner !== dt.current && (H = " It was passed a child from " + Xn(h._owner.type) + "."), Si(h), Re('Each child in a list should have a unique "key" prop.%s%s See https://reactjs.org/link/warning-keys for more information.', z, H), Si(null);
          }
        }
      }
      function Qt(h, C) {
        if (typeof h == "object") {
          if (_n(h))
            for (var z = 0; z < h.length; z++) {
              var H = h[z];
              hn(H) && cn(H, C);
            }
          else if (hn(h))
            h._store && (h._store.validated = !0);
          else if (h) {
            var Z = ht(h);
            if (typeof Z == "function" && Z !== h.entries)
              for (var Me = Z.call(h), le; !(le = Me.next()).done; )
                hn(le.value) && cn(le.value, C);
          }
        }
      }
      function wl(h) {
        {
          var C = h.type;
          if (C == null || typeof C == "string")
            return;
          var z;
          if (typeof C == "function")
            z = C.propTypes;
          else if (typeof C == "object" && (C.$$typeof === Ve || // Note: Memo only checks outer props here.
          // Inner props are checked in the reconciler.
          C.$$typeof === fe))
            z = C.propTypes;
          else
            return;
          if (z) {
            var H = Xn(C);
            Jo(z, h.props, "prop", H, h);
          } else if (C.PropTypes !== void 0 && !Qe) {
            Qe = !0;
            var Z = Xn(C);
            Re("Component %s declared `PropTypes` instead of `propTypes`. Did you misspell the property assignment?", Z || "Unknown");
          }
          typeof C.getDefaultProps == "function" && !C.getDefaultProps.isReactClassApproved && Re("getDefaultProps is only used on classic React.createClass definitions. Use a static property named `defaultProps` instead.");
        }
      }
      function Qn(h) {
        {
          for (var C = Object.keys(h.props), z = 0; z < C.length; z++) {
            var H = C[z];
            if (H !== "children" && H !== "key") {
              Si(h), Re("Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.", H), Si(null);
              break;
            }
          }
          h.ref !== null && (Si(h), Re("Invalid attribute `ref` supplied to `React.Fragment`."), Si(null));
        }
      }
      function Lr(h, C, z) {
        var H = I(h);
        if (!H) {
          var Z = "";
          (h === void 0 || typeof h == "object" && h !== null && Object.keys(h).length === 0) && (Z += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
          var Me = Ei(C);
          Me ? Z += Me : Z += lo();
          var le;
          h === null ? le = "null" : _n(h) ? le = "array" : h !== void 0 && h.$$typeof === oe ? (le = "<" + (Xn(h.type) || "Unknown") + " />", Z = " Did you accidentally export a JSX literal instead of a component?") : le = typeof h, Re("React.createElement: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: %s.%s", le, Z);
        }
        var Ae = it.apply(this, arguments);
        if (Ae == null)
          return Ae;
        if (H)
          for (var vt = 2; vt < arguments.length; vt++)
            Qt(arguments[vt], h);
        return h === He ? Qn(Ae) : wl(Ae), Ae;
      }
      var ka = !1;
      function du(h) {
        var C = Lr.bind(null, h);
        return C.type = h, ka || (ka = !0, Nt("React.createFactory() is deprecated and will be removed in a future major release. Consider using JSX or use React.createElement() directly instead.")), Object.defineProperty(C, "type", {
          enumerable: !1,
          get: function() {
            return Nt("Factory.type is deprecated. Access the class directly before passing it to createFactory."), Object.defineProperty(this, "type", {
              value: h
            }), h;
          }
        }), C;
      }
      function es(h, C, z) {
        for (var H = en.apply(this, arguments), Z = 2; Z < arguments.length; Z++)
          Qt(arguments[Z], H.type);
        return wl(H), H;
      }
      function ts(h, C) {
        var z = yt.transition;
        yt.transition = {};
        var H = yt.transition;
        yt.transition._updatedFibers = /* @__PURE__ */ new Set();
        try {
          h();
        } finally {
          if (yt.transition = z, z === null && H._updatedFibers) {
            var Z = H._updatedFibers.size;
            Z > 10 && Nt("Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table."), H._updatedFibers.clear();
          }
        }
      }
      var xl = !1, pu = null;
      function ed(h) {
        if (pu === null)
          try {
            var C = ("require" + Math.random()).slice(0, 7), z = O && O[C];
            pu = z.call(O, "timers").setImmediate;
          } catch {
            pu = function(Z) {
              xl === !1 && (xl = !0, typeof MessageChannel > "u" && Re("This browser does not have a MessageChannel implementation, so enqueuing tasks via await act(async () => ...) will fail. Please file an issue at https://github.com/facebook/react/issues if you encounter this warning."));
              var Me = new MessageChannel();
              Me.port1.onmessage = Z, Me.port2.postMessage(void 0);
            };
          }
        return pu(h);
      }
      var Da = 0, ri = !1;
      function _i(h) {
        {
          var C = Da;
          Da++, De.current === null && (De.current = []);
          var z = De.isBatchingLegacy, H;
          try {
            if (De.isBatchingLegacy = !0, H = h(), !z && De.didScheduleLegacyUpdate) {
              var Z = De.current;
              Z !== null && (De.didScheduleLegacyUpdate = !1, kl(Z));
            }
          } catch (lt) {
            throw Oa(C), lt;
          } finally {
            De.isBatchingLegacy = z;
          }
          if (H !== null && typeof H == "object" && typeof H.then == "function") {
            var Me = H, le = !1, Ae = {
              then: function(lt, Gt) {
                le = !0, Me.then(function(mn) {
                  Oa(C), Da === 0 ? uo(mn, lt, Gt) : lt(mn);
                }, function(mn) {
                  Oa(C), Gt(mn);
                });
              }
            };
            return !ri && typeof Promise < "u" && Promise.resolve().then(function() {
            }).then(function() {
              le || (ri = !0, Re("You called act(async () => ...) without await. This could lead to unexpected testing behaviour, interleaving multiple act calls and mixing their scopes. You should - await act(async () => ...);"));
            }), Ae;
          } else {
            var vt = H;
            if (Oa(C), Da === 0) {
              var xt = De.current;
              xt !== null && (kl(xt), De.current = null);
              var rn = {
                then: function(lt, Gt) {
                  De.current === null ? (De.current = [], uo(vt, lt, Gt)) : lt(vt);
                }
              };
              return rn;
            } else {
              var Wt = {
                then: function(lt, Gt) {
                  lt(vt);
                }
              };
              return Wt;
            }
          }
        }
      }
      function Oa(h) {
        h !== Da - 1 && Re("You seem to have overlapping act() calls, this is not supported. Be sure to await previous act() calls before making a new one. "), Da = h;
      }
      function uo(h, C, z) {
        {
          var H = De.current;
          if (H !== null)
            try {
              kl(H), ed(function() {
                H.length === 0 ? (De.current = null, C(h)) : uo(h, C, z);
              });
            } catch (Z) {
              z(Z);
            }
          else
            C(h);
        }
      }
      var oo = !1;
      function kl(h) {
        if (!oo) {
          oo = !0;
          var C = 0;
          try {
            for (; C < h.length; C++) {
              var z = h[C];
              do
                z = z(!0);
              while (z !== null);
            }
            h.length = 0;
          } catch (H) {
            throw h = h.slice(C + 1), H;
          } finally {
            oo = !1;
          }
        }
      }
      var vu = Lr, so = es, co = du, ai = {
        map: $i,
        forEach: uu,
        count: lu,
        toArray: El,
        only: Cl
      };
      A.Children = ai, A.Component = Fe, A.Fragment = He, A.Profiler = ft, A.PureComponent = ot, A.StrictMode = S, A.Suspense = te, A.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Dt, A.act = _i, A.cloneElement = so, A.createContext = ou, A.createElement = vu, A.createFactory = co, A.createRef = Nn, A.forwardRef = gi, A.isValidElement = hn, A.lazy = yi, A.memo = ue, A.startTransition = ts, A.unstable_act = _i, A.useCallback = lr, A.useContext = Ze, A.useDebugValue = Je, A.useDeferredValue = ei, A.useEffect = Tn, A.useId = su, A.useImperativeHandle = Ja, A.useInsertionEffect = nn, A.useLayoutEffect = sn, A.useMemo = Za, A.useReducer = pt, A.useRef = st, A.useState = We, A.useSyncExternalStore = cu, A.useTransition = nt, A.version = T, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(new Error());
    }();
  }(uv, uv.exports)), uv.exports;
}
process.env.NODE_ENV === "production" ? RE.exports = uk() : RE.exports = ok();
var Qr = RE.exports;
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oR;
function sk() {
  if (oR) return av;
  oR = 1;
  var O = Qr, A = Symbol.for("react.element"), T = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, ke = O.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, He = { key: !0, ref: !0, __self: !0, __source: !0 };
  function S(ft, ee, ne) {
    var Ve, te = {}, me = null, fe = null;
    ne !== void 0 && (me = "" + ne), ee.key !== void 0 && (me = "" + ee.key), ee.ref !== void 0 && (fe = ee.ref);
    for (Ve in ee) oe.call(ee, Ve) && !He.hasOwnProperty(Ve) && (te[Ve] = ee[Ve]);
    if (ft && ft.defaultProps) for (Ve in ee = ft.defaultProps, ee) te[Ve] === void 0 && (te[Ve] = ee[Ve]);
    return { $$typeof: A, type: ft, key: me, ref: fe, props: te, _owner: ke.current };
  }
  return av.Fragment = T, av.jsx = S, av.jsxs = S, av;
}
var iv = {};
/**
 * @license React
 * react-jsx-runtime.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var sR;
function ck() {
  return sR || (sR = 1, process.env.NODE_ENV !== "production" && function() {
    var O = Qr, A = Symbol.for("react.element"), T = Symbol.for("react.portal"), oe = Symbol.for("react.fragment"), ke = Symbol.for("react.strict_mode"), He = Symbol.for("react.profiler"), S = Symbol.for("react.provider"), ft = Symbol.for("react.context"), ee = Symbol.for("react.forward_ref"), ne = Symbol.for("react.suspense"), Ve = Symbol.for("react.suspense_list"), te = Symbol.for("react.memo"), me = Symbol.for("react.lazy"), fe = Symbol.for("react.offscreen"), qe = Symbol.iterator, Et = "@@iterator";
    function mt(_) {
      if (_ === null || typeof _ != "object")
        return null;
      var I = qe && _[qe] || _[Et];
      return typeof I == "function" ? I : null;
    }
    var dn = O.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
    function ht(_) {
      {
        for (var I = arguments.length, ue = new Array(I > 1 ? I - 1 : 0), ge = 1; ge < I; ge++)
          ue[ge - 1] = arguments[ge];
        Ke("error", _, ue);
      }
    }
    function Ke(_, I, ue) {
      {
        var ge = dn.ReactDebugCurrentFrame, Ze = ge.getStackAddendum();
        Ze !== "" && (I += "%s", ue = ue.concat([Ze]));
        var We = ue.map(function(pt) {
          return String(pt);
        });
        We.unshift("Warning: " + I), Function.prototype.apply.call(console[_], console, We);
      }
    }
    var yt = !1, De = !1, dt = !1, Be = !1, ln = !1, Vt;
    Vt = Symbol.for("react.module.reference");
    function Jt(_) {
      return !!(typeof _ == "string" || typeof _ == "function" || _ === oe || _ === He || ln || _ === ke || _ === ne || _ === Ve || Be || _ === fe || yt || De || dt || typeof _ == "object" && _ !== null && (_.$$typeof === me || _.$$typeof === te || _.$$typeof === S || _.$$typeof === ft || _.$$typeof === ee || // This needs to include all possible module reference object
      // types supported by any Flight configuration anywhere since
      // we don't know which Flight build this will end up being used
      // with.
      _.$$typeof === Vt || _.getModuleId !== void 0));
    }
    function un(_, I, ue) {
      var ge = _.displayName;
      if (ge)
        return ge;
      var Ze = I.displayName || I.name || "";
      return Ze !== "" ? ue + "(" + Ze + ")" : ue;
    }
    function kt(_) {
      return _.displayName || "Context";
    }
    function Le(_) {
      if (_ == null)
        return null;
      if (typeof _.tag == "number" && ht("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof _ == "function")
        return _.displayName || _.name || null;
      if (typeof _ == "string")
        return _;
      switch (_) {
        case oe:
          return "Fragment";
        case T:
          return "Portal";
        case He:
          return "Profiler";
        case ke:
          return "StrictMode";
        case ne:
          return "Suspense";
        case Ve:
          return "SuspenseList";
      }
      if (typeof _ == "object")
        switch (_.$$typeof) {
          case ft:
            var I = _;
            return kt(I) + ".Consumer";
          case S:
            var ue = _;
            return kt(ue._context) + ".Provider";
          case ee:
            return un(_, _.render, "ForwardRef");
          case te:
            var ge = _.displayName || null;
            return ge !== null ? ge : Le(_.type) || "Memo";
          case me: {
            var Ze = _, We = Ze._payload, pt = Ze._init;
            try {
              return Le(pt(We));
            } catch {
              return null;
            }
          }
        }
      return null;
    }
    var Ft = Object.assign, Dt = 0, Nt, Re, J, Te, ie, k, B;
    function $e() {
    }
    $e.__reactDisabledLog = !0;
    function Fe() {
      {
        if (Dt === 0) {
          Nt = console.log, Re = console.info, J = console.warn, Te = console.error, ie = console.group, k = console.groupCollapsed, B = console.groupEnd;
          var _ = {
            configurable: !0,
            enumerable: !0,
            value: $e,
            writable: !0
          };
          Object.defineProperties(console, {
            info: _,
            log: _,
            warn: _,
            error: _,
            group: _,
            groupCollapsed: _,
            groupEnd: _
          });
        }
        Dt++;
      }
    }
    function ut() {
      {
        if (Dt--, Dt === 0) {
          var _ = {
            configurable: !0,
            enumerable: !0,
            writable: !0
          };
          Object.defineProperties(console, {
            log: Ft({}, _, {
              value: Nt
            }),
            info: Ft({}, _, {
              value: Re
            }),
            warn: Ft({}, _, {
              value: J
            }),
            error: Ft({}, _, {
              value: Te
            }),
            group: Ft({}, _, {
              value: ie
            }),
            groupCollapsed: Ft({}, _, {
              value: k
            }),
            groupEnd: Ft({}, _, {
              value: B
            })
          });
        }
        Dt < 0 && ht("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
      }
    }
    var rt = dn.ReactCurrentDispatcher, tt;
    function at(_, I, ue) {
      {
        if (tt === void 0)
          try {
            throw Error();
          } catch (Ze) {
            var ge = Ze.stack.trim().match(/\n( *(at )?)/);
            tt = ge && ge[1] || "";
          }
        return `
` + tt + _;
      }
    }
    var ot = !1, $t;
    {
      var Nn = typeof WeakMap == "function" ? WeakMap : Map;
      $t = new Nn();
    }
    function xr(_, I) {
      if (!_ || ot)
        return "";
      {
        var ue = $t.get(_);
        if (ue !== void 0)
          return ue;
      }
      var ge;
      ot = !0;
      var Ze = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      var We;
      We = rt.current, rt.current = null, Fe();
      try {
        if (I) {
          var pt = function() {
            throw Error();
          };
          if (Object.defineProperty(pt.prototype, "props", {
            set: function() {
              throw Error();
            }
          }), typeof Reflect == "object" && Reflect.construct) {
            try {
              Reflect.construct(pt, []);
            } catch (Je) {
              ge = Je;
            }
            Reflect.construct(_, [], pt);
          } else {
            try {
              pt.call();
            } catch (Je) {
              ge = Je;
            }
            _.call(pt.prototype);
          }
        } else {
          try {
            throw Error();
          } catch (Je) {
            ge = Je;
          }
          _();
        }
      } catch (Je) {
        if (Je && ge && typeof Je.stack == "string") {
          for (var st = Je.stack.split(`
`), Tn = ge.stack.split(`
`), nn = st.length - 1, sn = Tn.length - 1; nn >= 1 && sn >= 0 && st[nn] !== Tn[sn]; )
            sn--;
          for (; nn >= 1 && sn >= 0; nn--, sn--)
            if (st[nn] !== Tn[sn]) {
              if (nn !== 1 || sn !== 1)
                do
                  if (nn--, sn--, sn < 0 || st[nn] !== Tn[sn]) {
                    var lr = `
` + st[nn].replace(" at new ", " at ");
                    return _.displayName && lr.includes("<anonymous>") && (lr = lr.replace("<anonymous>", _.displayName)), typeof _ == "function" && $t.set(_, lr), lr;
                  }
                while (nn >= 1 && sn >= 0);
              break;
            }
        }
      } finally {
        ot = !1, rt.current = We, ut(), Error.prepareStackTrace = Ze;
      }
      var Za = _ ? _.displayName || _.name : "", Ja = Za ? at(Za) : "";
      return typeof _ == "function" && $t.set(_, Ja), Ja;
    }
    function _n(_, I, ue) {
      return xr(_, !1);
    }
    function ar(_) {
      var I = _.prototype;
      return !!(I && I.isReactComponent);
    }
    function $n(_, I, ue) {
      if (_ == null)
        return "";
      if (typeof _ == "function")
        return xr(_, ar(_));
      if (typeof _ == "string")
        return at(_);
      switch (_) {
        case ne:
          return at("Suspense");
        case Ve:
          return at("SuspenseList");
      }
      if (typeof _ == "object")
        switch (_.$$typeof) {
          case ee:
            return _n(_.render);
          case te:
            return $n(_.type, I, ue);
          case me: {
            var ge = _, Ze = ge._payload, We = ge._init;
            try {
              return $n(We(Ze), I, ue);
            } catch {
            }
          }
        }
      return "";
    }
    var In = Object.prototype.hasOwnProperty, Wr = {}, vi = dn.ReactDebugCurrentFrame;
    function fa(_) {
      if (_) {
        var I = _._owner, ue = $n(_.type, _._source, I ? I.type : null);
        vi.setExtraStackFrame(ue);
      } else
        vi.setExtraStackFrame(null);
    }
    function Xn(_, I, ue, ge, Ze) {
      {
        var We = Function.call.bind(In);
        for (var pt in _)
          if (We(_, pt)) {
            var st = void 0;
            try {
              if (typeof _[pt] != "function") {
                var Tn = Error((ge || "React class") + ": " + ue + " type `" + pt + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof _[pt] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                throw Tn.name = "Invariant Violation", Tn;
              }
              st = _[pt](I, pt, ge, ue, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
            } catch (nn) {
              st = nn;
            }
            st && !(st instanceof Error) && (fa(Ze), ht("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", ge || "React class", ue, pt, typeof st), fa(null)), st instanceof Error && !(st.message in Wr) && (Wr[st.message] = !0, fa(Ze), ht("Failed %s type: %s", ue, st.message), fa(null));
          }
      }
    }
    var Rn = Array.isArray;
    function Yn(_) {
      return Rn(_);
    }
    function Er(_) {
      {
        var I = typeof Symbol == "function" && Symbol.toStringTag, ue = I && _[Symbol.toStringTag] || _.constructor.name || "Object";
        return ue;
      }
    }
    function qa(_) {
      try {
        return Ln(_), !1;
      } catch {
        return !0;
      }
    }
    function Ln(_) {
      return "" + _;
    }
    function Cr(_) {
      if (qa(_))
        return ht("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", Er(_)), Ln(_);
    }
    var da = dn.ReactCurrentOwner, Ka = {
      key: !0,
      ref: !0,
      __self: !0,
      __source: !0
    }, hi, re;
    function be(_) {
      if (In.call(_, "ref")) {
        var I = Object.getOwnPropertyDescriptor(_, "ref").get;
        if (I && I.isReactWarning)
          return !1;
      }
      return _.ref !== void 0;
    }
    function it(_) {
      if (In.call(_, "key")) {
        var I = Object.getOwnPropertyDescriptor(_, "key").get;
        if (I && I.isReactWarning)
          return !1;
      }
      return _.key !== void 0;
    }
    function Ht(_, I) {
      typeof _.ref == "string" && da.current;
    }
    function en(_, I) {
      {
        var ue = function() {
          hi || (hi = !0, ht("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", I));
        };
        ue.isReactWarning = !0, Object.defineProperty(_, "key", {
          get: ue,
          configurable: !0
        });
      }
    }
    function hn(_, I) {
      {
        var ue = function() {
          re || (re = !0, ht("%s: `ref` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", I));
        };
        ue.isReactWarning = !0, Object.defineProperty(_, "ref", {
          get: ue,
          configurable: !0
        });
      }
    }
    var on = function(_, I, ue, ge, Ze, We, pt) {
      var st = {
        // This tag allows us to uniquely identify this as a React Element
        $$typeof: A,
        // Built-in properties that belong on the element
        type: _,
        key: I,
        ref: ue,
        props: pt,
        // Record the component responsible for creating this element.
        _owner: We
      };
      return st._store = {}, Object.defineProperty(st._store, "validated", {
        configurable: !1,
        enumerable: !1,
        writable: !0,
        value: !1
      }), Object.defineProperty(st, "_self", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: ge
      }), Object.defineProperty(st, "_source", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: Ze
      }), Object.freeze && (Object.freeze(st.props), Object.freeze(st)), st;
    };
    function Zn(_, I, ue, ge, Ze) {
      {
        var We, pt = {}, st = null, Tn = null;
        ue !== void 0 && (Cr(ue), st = "" + ue), it(I) && (Cr(I.key), st = "" + I.key), be(I) && (Tn = I.ref, Ht(I, Ze));
        for (We in I)
          In.call(I, We) && !Ka.hasOwnProperty(We) && (pt[We] = I[We]);
        if (_ && _.defaultProps) {
          var nn = _.defaultProps;
          for (We in nn)
            pt[We] === void 0 && (pt[We] = nn[We]);
        }
        if (st || Tn) {
          var sn = typeof _ == "function" ? _.displayName || _.name || "Unknown" : _;
          st && en(pt, sn), Tn && hn(pt, sn);
        }
        return on(_, st, Tn, Ze, ge, da.current, pt);
      }
    }
    var tn = dn.ReactCurrentOwner, It = dn.ReactDebugCurrentFrame;
    function Yt(_) {
      if (_) {
        var I = _._owner, ue = $n(_.type, _._source, I ? I.type : null);
        It.setExtraStackFrame(ue);
      } else
        It.setExtraStackFrame(null);
    }
    var pa;
    pa = !1;
    function _r(_) {
      return typeof _ == "object" && _ !== null && _.$$typeof === A;
    }
    function xa() {
      {
        if (tn.current) {
          var _ = Le(tn.current.type);
          if (_)
            return `

Check the render method of \`` + _ + "`.";
        }
        return "";
      }
    }
    function $i(_) {
      return "";
    }
    var lu = {};
    function uu(_) {
      {
        var I = xa();
        if (!I) {
          var ue = typeof _ == "string" ? _ : _.displayName || _.name;
          ue && (I = `

Check the top-level render call using <` + ue + ">.");
        }
        return I;
      }
    }
    function El(_, I) {
      {
        if (!_._store || _._store.validated || _.key != null)
          return;
        _._store.validated = !0;
        var ue = uu(I);
        if (lu[ue])
          return;
        lu[ue] = !0;
        var ge = "";
        _ && _._owner && _._owner !== tn.current && (ge = " It was passed a child from " + Le(_._owner.type) + "."), Yt(_), ht('Each child in a list should have a unique "key" prop.%s%s See https://reactjs.org/link/warning-keys for more information.', ue, ge), Yt(null);
      }
    }
    function Cl(_, I) {
      {
        if (typeof _ != "object")
          return;
        if (Yn(_))
          for (var ue = 0; ue < _.length; ue++) {
            var ge = _[ue];
            _r(ge) && El(ge, I);
          }
        else if (_r(_))
          _._store && (_._store.validated = !0);
        else if (_) {
          var Ze = mt(_);
          if (typeof Ze == "function" && Ze !== _.entries)
            for (var We = Ze.call(_), pt; !(pt = We.next()).done; )
              _r(pt.value) && El(pt.value, I);
        }
      }
    }
    function ou(_) {
      {
        var I = _.type;
        if (I == null || typeof I == "string")
          return;
        var ue;
        if (typeof I == "function")
          ue = I.propTypes;
        else if (typeof I == "object" && (I.$$typeof === ee || // Note: Memo only checks outer props here.
        // Inner props are checked in the reconciler.
        I.$$typeof === te))
          ue = I.propTypes;
        else
          return;
        if (ue) {
          var ge = Le(I);
          Xn(ue, _.props, "prop", ge, _);
        } else if (I.PropTypes !== void 0 && !pa) {
          pa = !0;
          var Ze = Le(I);
          ht("Component %s declared `PropTypes` instead of `propTypes`. Did you misspell the property assignment?", Ze || "Unknown");
        }
        typeof I.getDefaultProps == "function" && !I.getDefaultProps.isReactClassApproved && ht("getDefaultProps is only used on classic React.createClass definitions. Use a static property named `defaultProps` instead.");
      }
    }
    function kr(_) {
      {
        for (var I = Object.keys(_.props), ue = 0; ue < I.length; ue++) {
          var ge = I[ue];
          if (ge !== "children" && ge !== "key") {
            Yt(_), ht("Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.", ge), Yt(null);
            break;
          }
        }
        _.ref !== null && (Yt(_), ht("Invalid attribute `ref` supplied to `React.Fragment`."), Yt(null));
      }
    }
    var Dr = {};
    function ir(_, I, ue, ge, Ze, We) {
      {
        var pt = Jt(_);
        if (!pt) {
          var st = "";
          (_ === void 0 || typeof _ == "object" && _ !== null && Object.keys(_).length === 0) && (st += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
          var Tn = $i();
          Tn ? st += Tn : st += xa();
          var nn;
          _ === null ? nn = "null" : Yn(_) ? nn = "array" : _ !== void 0 && _.$$typeof === A ? (nn = "<" + (Le(_.type) || "Unknown") + " />", st = " Did you accidentally export a JSX literal instead of a component?") : nn = typeof _, ht("React.jsx: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: %s.%s", nn, st);
        }
        var sn = Zn(_, I, ue, Ze, We);
        if (sn == null)
          return sn;
        if (pt) {
          var lr = I.children;
          if (lr !== void 0)
            if (ge)
              if (Yn(lr)) {
                for (var Za = 0; Za < lr.length; Za++)
                  Cl(lr[Za], _);
                Object.freeze && Object.freeze(lr);
              } else
                ht("React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead.");
            else
              Cl(lr, _);
        }
        if (In.call(I, "key")) {
          var Ja = Le(_), Je = Object.keys(I).filter(function(su) {
            return su !== "key";
          }), nt = Je.length > 0 ? "{key: someKey, " + Je.join(": ..., ") + ": ...}" : "{key: someKey}";
          if (!Dr[Ja + nt]) {
            var ei = Je.length > 0 ? "{" + Je.join(": ..., ") + ": ...}" : "{}";
            ht(`A props object containing a "key" prop is being spread into JSX:
  let props = %s;
  <%s {...props} />
React keys must be passed directly to JSX without using spread:
  let props = %s;
  <%s key={someKey} {...props} />`, nt, Ja, ei, Ja), Dr[Ja + nt] = !0;
          }
        }
        return _ === oe ? kr(sn) : ou(sn), sn;
      }
    }
    function mi(_, I, ue) {
      return ir(_, I, ue, !0);
    }
    function Xa(_, I, ue) {
      return ir(_, I, ue, !1);
    }
    var yi = Xa, gi = mi;
    iv.Fragment = oe, iv.jsx = yi, iv.jsxs = gi;
  }()), iv;
}
process.env.NODE_ENV === "production" ? _E.exports = sk() : _E.exports = ck();
var X = _E.exports, TE = { exports: {} }, Qa = {}, Jm = { exports: {} }, EE = {};
/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var cR;
function fk() {
  return cR || (cR = 1, function(O) {
    function A(J, Te) {
      var ie = J.length;
      J.push(Te);
      e: for (; 0 < ie; ) {
        var k = ie - 1 >>> 1, B = J[k];
        if (0 < ke(B, Te)) J[k] = Te, J[ie] = B, ie = k;
        else break e;
      }
    }
    function T(J) {
      return J.length === 0 ? null : J[0];
    }
    function oe(J) {
      if (J.length === 0) return null;
      var Te = J[0], ie = J.pop();
      if (ie !== Te) {
        J[0] = ie;
        e: for (var k = 0, B = J.length, $e = B >>> 1; k < $e; ) {
          var Fe = 2 * (k + 1) - 1, ut = J[Fe], rt = Fe + 1, tt = J[rt];
          if (0 > ke(ut, ie)) rt < B && 0 > ke(tt, ut) ? (J[k] = tt, J[rt] = ie, k = rt) : (J[k] = ut, J[Fe] = ie, k = Fe);
          else if (rt < B && 0 > ke(tt, ie)) J[k] = tt, J[rt] = ie, k = rt;
          else break e;
        }
      }
      return Te;
    }
    function ke(J, Te) {
      var ie = J.sortIndex - Te.sortIndex;
      return ie !== 0 ? ie : J.id - Te.id;
    }
    if (typeof performance == "object" && typeof performance.now == "function") {
      var He = performance;
      O.unstable_now = function() {
        return He.now();
      };
    } else {
      var S = Date, ft = S.now();
      O.unstable_now = function() {
        return S.now() - ft;
      };
    }
    var ee = [], ne = [], Ve = 1, te = null, me = 3, fe = !1, qe = !1, Et = !1, mt = typeof setTimeout == "function" ? setTimeout : null, dn = typeof clearTimeout == "function" ? clearTimeout : null, ht = typeof setImmediate < "u" ? setImmediate : null;
    typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
    function Ke(J) {
      for (var Te = T(ne); Te !== null; ) {
        if (Te.callback === null) oe(ne);
        else if (Te.startTime <= J) oe(ne), Te.sortIndex = Te.expirationTime, A(ee, Te);
        else break;
        Te = T(ne);
      }
    }
    function yt(J) {
      if (Et = !1, Ke(J), !qe) if (T(ee) !== null) qe = !0, Nt(De);
      else {
        var Te = T(ne);
        Te !== null && Re(yt, Te.startTime - J);
      }
    }
    function De(J, Te) {
      qe = !1, Et && (Et = !1, dn(ln), ln = -1), fe = !0;
      var ie = me;
      try {
        for (Ke(Te), te = T(ee); te !== null && (!(te.expirationTime > Te) || J && !un()); ) {
          var k = te.callback;
          if (typeof k == "function") {
            te.callback = null, me = te.priorityLevel;
            var B = k(te.expirationTime <= Te);
            Te = O.unstable_now(), typeof B == "function" ? te.callback = B : te === T(ee) && oe(ee), Ke(Te);
          } else oe(ee);
          te = T(ee);
        }
        if (te !== null) var $e = !0;
        else {
          var Fe = T(ne);
          Fe !== null && Re(yt, Fe.startTime - Te), $e = !1;
        }
        return $e;
      } finally {
        te = null, me = ie, fe = !1;
      }
    }
    var dt = !1, Be = null, ln = -1, Vt = 5, Jt = -1;
    function un() {
      return !(O.unstable_now() - Jt < Vt);
    }
    function kt() {
      if (Be !== null) {
        var J = O.unstable_now();
        Jt = J;
        var Te = !0;
        try {
          Te = Be(!0, J);
        } finally {
          Te ? Le() : (dt = !1, Be = null);
        }
      } else dt = !1;
    }
    var Le;
    if (typeof ht == "function") Le = function() {
      ht(kt);
    };
    else if (typeof MessageChannel < "u") {
      var Ft = new MessageChannel(), Dt = Ft.port2;
      Ft.port1.onmessage = kt, Le = function() {
        Dt.postMessage(null);
      };
    } else Le = function() {
      mt(kt, 0);
    };
    function Nt(J) {
      Be = J, dt || (dt = !0, Le());
    }
    function Re(J, Te) {
      ln = mt(function() {
        J(O.unstable_now());
      }, Te);
    }
    O.unstable_IdlePriority = 5, O.unstable_ImmediatePriority = 1, O.unstable_LowPriority = 4, O.unstable_NormalPriority = 3, O.unstable_Profiling = null, O.unstable_UserBlockingPriority = 2, O.unstable_cancelCallback = function(J) {
      J.callback = null;
    }, O.unstable_continueExecution = function() {
      qe || fe || (qe = !0, Nt(De));
    }, O.unstable_forceFrameRate = function(J) {
      0 > J || 125 < J ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : Vt = 0 < J ? Math.floor(1e3 / J) : 5;
    }, O.unstable_getCurrentPriorityLevel = function() {
      return me;
    }, O.unstable_getFirstCallbackNode = function() {
      return T(ee);
    }, O.unstable_next = function(J) {
      switch (me) {
        case 1:
        case 2:
        case 3:
          var Te = 3;
          break;
        default:
          Te = me;
      }
      var ie = me;
      me = Te;
      try {
        return J();
      } finally {
        me = ie;
      }
    }, O.unstable_pauseExecution = function() {
    }, O.unstable_requestPaint = function() {
    }, O.unstable_runWithPriority = function(J, Te) {
      switch (J) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
          break;
        default:
          J = 3;
      }
      var ie = me;
      me = J;
      try {
        return Te();
      } finally {
        me = ie;
      }
    }, O.unstable_scheduleCallback = function(J, Te, ie) {
      var k = O.unstable_now();
      switch (typeof ie == "object" && ie !== null ? (ie = ie.delay, ie = typeof ie == "number" && 0 < ie ? k + ie : k) : ie = k, J) {
        case 1:
          var B = -1;
          break;
        case 2:
          B = 250;
          break;
        case 5:
          B = 1073741823;
          break;
        case 4:
          B = 1e4;
          break;
        default:
          B = 5e3;
      }
      return B = ie + B, J = { id: Ve++, callback: Te, priorityLevel: J, startTime: ie, expirationTime: B, sortIndex: -1 }, ie > k ? (J.sortIndex = ie, A(ne, J), T(ee) === null && J === T(ne) && (Et ? (dn(ln), ln = -1) : Et = !0, Re(yt, ie - k))) : (J.sortIndex = B, A(ee, J), qe || fe || (qe = !0, Nt(De))), J;
    }, O.unstable_shouldYield = un, O.unstable_wrapCallback = function(J) {
      var Te = me;
      return function() {
        var ie = me;
        me = Te;
        try {
          return J.apply(this, arguments);
        } finally {
          me = ie;
        }
      };
    };
  }(EE)), EE;
}
var CE = {};
/**
 * @license React
 * scheduler.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var fR;
function dk() {
  return fR || (fR = 1, function(O) {
    process.env.NODE_ENV !== "production" && function() {
      typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(new Error());
      var A = !1, T = 5;
      function oe(re, be) {
        var it = re.length;
        re.push(be), S(re, be, it);
      }
      function ke(re) {
        return re.length === 0 ? null : re[0];
      }
      function He(re) {
        if (re.length === 0)
          return null;
        var be = re[0], it = re.pop();
        return it !== be && (re[0] = it, ft(re, it, 0)), be;
      }
      function S(re, be, it) {
        for (var Ht = it; Ht > 0; ) {
          var en = Ht - 1 >>> 1, hn = re[en];
          if (ee(hn, be) > 0)
            re[en] = be, re[Ht] = hn, Ht = en;
          else
            return;
        }
      }
      function ft(re, be, it) {
        for (var Ht = it, en = re.length, hn = en >>> 1; Ht < hn; ) {
          var on = (Ht + 1) * 2 - 1, Zn = re[on], tn = on + 1, It = re[tn];
          if (ee(Zn, be) < 0)
            tn < en && ee(It, Zn) < 0 ? (re[Ht] = It, re[tn] = be, Ht = tn) : (re[Ht] = Zn, re[on] = be, Ht = on);
          else if (tn < en && ee(It, be) < 0)
            re[Ht] = It, re[tn] = be, Ht = tn;
          else
            return;
        }
      }
      function ee(re, be) {
        var it = re.sortIndex - be.sortIndex;
        return it !== 0 ? it : re.id - be.id;
      }
      var ne = 1, Ve = 2, te = 3, me = 4, fe = 5;
      function qe(re, be) {
      }
      var Et = typeof performance == "object" && typeof performance.now == "function";
      if (Et) {
        var mt = performance;
        O.unstable_now = function() {
          return mt.now();
        };
      } else {
        var dn = Date, ht = dn.now();
        O.unstable_now = function() {
          return dn.now() - ht;
        };
      }
      var Ke = 1073741823, yt = -1, De = 250, dt = 5e3, Be = 1e4, ln = Ke, Vt = [], Jt = [], un = 1, kt = null, Le = te, Ft = !1, Dt = !1, Nt = !1, Re = typeof setTimeout == "function" ? setTimeout : null, J = typeof clearTimeout == "function" ? clearTimeout : null, Te = typeof setImmediate < "u" ? setImmediate : null;
      typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
      function ie(re) {
        for (var be = ke(Jt); be !== null; ) {
          if (be.callback === null)
            He(Jt);
          else if (be.startTime <= re)
            He(Jt), be.sortIndex = be.expirationTime, oe(Vt, be);
          else
            return;
          be = ke(Jt);
        }
      }
      function k(re) {
        if (Nt = !1, ie(re), !Dt)
          if (ke(Vt) !== null)
            Dt = !0, Ln(B);
          else {
            var be = ke(Jt);
            be !== null && Cr(k, be.startTime - re);
          }
      }
      function B(re, be) {
        Dt = !1, Nt && (Nt = !1, da()), Ft = !0;
        var it = Le;
        try {
          var Ht;
          if (!A) return $e(re, be);
        } finally {
          kt = null, Le = it, Ft = !1;
        }
      }
      function $e(re, be) {
        var it = be;
        for (ie(it), kt = ke(Vt); kt !== null && !(kt.expirationTime > it && (!re || vi())); ) {
          var Ht = kt.callback;
          if (typeof Ht == "function") {
            kt.callback = null, Le = kt.priorityLevel;
            var en = kt.expirationTime <= it, hn = Ht(en);
            it = O.unstable_now(), typeof hn == "function" ? kt.callback = hn : kt === ke(Vt) && He(Vt), ie(it);
          } else
            He(Vt);
          kt = ke(Vt);
        }
        if (kt !== null)
          return !0;
        var on = ke(Jt);
        return on !== null && Cr(k, on.startTime - it), !1;
      }
      function Fe(re, be) {
        switch (re) {
          case ne:
          case Ve:
          case te:
          case me:
          case fe:
            break;
          default:
            re = te;
        }
        var it = Le;
        Le = re;
        try {
          return be();
        } finally {
          Le = it;
        }
      }
      function ut(re) {
        var be;
        switch (Le) {
          case ne:
          case Ve:
          case te:
            be = te;
            break;
          default:
            be = Le;
            break;
        }
        var it = Le;
        Le = be;
        try {
          return re();
        } finally {
          Le = it;
        }
      }
      function rt(re) {
        var be = Le;
        return function() {
          var it = Le;
          Le = be;
          try {
            return re.apply(this, arguments);
          } finally {
            Le = it;
          }
        };
      }
      function tt(re, be, it) {
        var Ht = O.unstable_now(), en;
        if (typeof it == "object" && it !== null) {
          var hn = it.delay;
          typeof hn == "number" && hn > 0 ? en = Ht + hn : en = Ht;
        } else
          en = Ht;
        var on;
        switch (re) {
          case ne:
            on = yt;
            break;
          case Ve:
            on = De;
            break;
          case fe:
            on = ln;
            break;
          case me:
            on = Be;
            break;
          case te:
          default:
            on = dt;
            break;
        }
        var Zn = en + on, tn = {
          id: un++,
          callback: be,
          priorityLevel: re,
          startTime: en,
          expirationTime: Zn,
          sortIndex: -1
        };
        return en > Ht ? (tn.sortIndex = en, oe(Jt, tn), ke(Vt) === null && tn === ke(Jt) && (Nt ? da() : Nt = !0, Cr(k, en - Ht))) : (tn.sortIndex = Zn, oe(Vt, tn), !Dt && !Ft && (Dt = !0, Ln(B))), tn;
      }
      function at() {
      }
      function ot() {
        !Dt && !Ft && (Dt = !0, Ln(B));
      }
      function $t() {
        return ke(Vt);
      }
      function Nn(re) {
        re.callback = null;
      }
      function xr() {
        return Le;
      }
      var _n = !1, ar = null, $n = -1, In = T, Wr = -1;
      function vi() {
        var re = O.unstable_now() - Wr;
        return !(re < In);
      }
      function fa() {
      }
      function Xn(re) {
        if (re < 0 || re > 125) {
          console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported");
          return;
        }
        re > 0 ? In = Math.floor(1e3 / re) : In = T;
      }
      var Rn = function() {
        if (ar !== null) {
          var re = O.unstable_now();
          Wr = re;
          var be = !0, it = !0;
          try {
            it = ar(be, re);
          } finally {
            it ? Yn() : (_n = !1, ar = null);
          }
        } else
          _n = !1;
      }, Yn;
      if (typeof Te == "function")
        Yn = function() {
          Te(Rn);
        };
      else if (typeof MessageChannel < "u") {
        var Er = new MessageChannel(), qa = Er.port2;
        Er.port1.onmessage = Rn, Yn = function() {
          qa.postMessage(null);
        };
      } else
        Yn = function() {
          Re(Rn, 0);
        };
      function Ln(re) {
        ar = re, _n || (_n = !0, Yn());
      }
      function Cr(re, be) {
        $n = Re(function() {
          re(O.unstable_now());
        }, be);
      }
      function da() {
        J($n), $n = -1;
      }
      var Ka = fa, hi = null;
      O.unstable_IdlePriority = fe, O.unstable_ImmediatePriority = ne, O.unstable_LowPriority = me, O.unstable_NormalPriority = te, O.unstable_Profiling = hi, O.unstable_UserBlockingPriority = Ve, O.unstable_cancelCallback = Nn, O.unstable_continueExecution = ot, O.unstable_forceFrameRate = Xn, O.unstable_getCurrentPriorityLevel = xr, O.unstable_getFirstCallbackNode = $t, O.unstable_next = ut, O.unstable_pauseExecution = at, O.unstable_requestPaint = Ka, O.unstable_runWithPriority = Fe, O.unstable_scheduleCallback = tt, O.unstable_shouldYield = vi, O.unstable_wrapCallback = rt, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(new Error());
    }();
  }(CE)), CE;
}
var dR;
function SR() {
  return dR || (dR = 1, process.env.NODE_ENV === "production" ? Jm.exports = fk() : Jm.exports = dk()), Jm.exports;
}
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var pR;
function pk() {
  if (pR) return Qa;
  pR = 1;
  var O = Qr, A = SR();
  function T(n) {
    for (var r = "https://reactjs.org/docs/error-decoder.html?invariant=" + n, l = 1; l < arguments.length; l++) r += "&args[]=" + encodeURIComponent(arguments[l]);
    return "Minified React error #" + n + "; visit " + r + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  var oe = /* @__PURE__ */ new Set(), ke = {};
  function He(n, r) {
    S(n, r), S(n + "Capture", r);
  }
  function S(n, r) {
    for (ke[n] = r, n = 0; n < r.length; n++) oe.add(r[n]);
  }
  var ft = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), ee = Object.prototype.hasOwnProperty, ne = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, Ve = {}, te = {};
  function me(n) {
    return ee.call(te, n) ? !0 : ee.call(Ve, n) ? !1 : ne.test(n) ? te[n] = !0 : (Ve[n] = !0, !1);
  }
  function fe(n, r, l, o) {
    if (l !== null && l.type === 0) return !1;
    switch (typeof r) {
      case "function":
      case "symbol":
        return !0;
      case "boolean":
        return o ? !1 : l !== null ? !l.acceptsBooleans : (n = n.toLowerCase().slice(0, 5), n !== "data-" && n !== "aria-");
      default:
        return !1;
    }
  }
  function qe(n, r, l, o) {
    if (r === null || typeof r > "u" || fe(n, r, l, o)) return !0;
    if (o) return !1;
    if (l !== null) switch (l.type) {
      case 3:
        return !r;
      case 4:
        return r === !1;
      case 5:
        return isNaN(r);
      case 6:
        return isNaN(r) || 1 > r;
    }
    return !1;
  }
  function Et(n, r, l, o, c, d, m) {
    this.acceptsBooleans = r === 2 || r === 3 || r === 4, this.attributeName = o, this.attributeNamespace = c, this.mustUseProperty = l, this.propertyName = n, this.type = r, this.sanitizeURL = d, this.removeEmptyString = m;
  }
  var mt = {};
  "children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(n) {
    mt[n] = new Et(n, 0, !1, n, null, !1, !1);
  }), [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(n) {
    var r = n[0];
    mt[r] = new Et(r, 1, !1, n[1], null, !1, !1);
  }), ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(n) {
    mt[n] = new Et(n, 2, !1, n.toLowerCase(), null, !1, !1);
  }), ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(n) {
    mt[n] = new Et(n, 2, !1, n, null, !1, !1);
  }), "allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(n) {
    mt[n] = new Et(n, 3, !1, n.toLowerCase(), null, !1, !1);
  }), ["checked", "multiple", "muted", "selected"].forEach(function(n) {
    mt[n] = new Et(n, 3, !0, n, null, !1, !1);
  }), ["capture", "download"].forEach(function(n) {
    mt[n] = new Et(n, 4, !1, n, null, !1, !1);
  }), ["cols", "rows", "size", "span"].forEach(function(n) {
    mt[n] = new Et(n, 6, !1, n, null, !1, !1);
  }), ["rowSpan", "start"].forEach(function(n) {
    mt[n] = new Et(n, 5, !1, n.toLowerCase(), null, !1, !1);
  });
  var dn = /[\-:]([a-z])/g;
  function ht(n) {
    return n[1].toUpperCase();
  }
  "accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(n) {
    var r = n.replace(
      dn,
      ht
    );
    mt[r] = new Et(r, 1, !1, n, null, !1, !1);
  }), "xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(n) {
    var r = n.replace(dn, ht);
    mt[r] = new Et(r, 1, !1, n, "http://www.w3.org/1999/xlink", !1, !1);
  }), ["xml:base", "xml:lang", "xml:space"].forEach(function(n) {
    var r = n.replace(dn, ht);
    mt[r] = new Et(r, 1, !1, n, "http://www.w3.org/XML/1998/namespace", !1, !1);
  }), ["tabIndex", "crossOrigin"].forEach(function(n) {
    mt[n] = new Et(n, 1, !1, n.toLowerCase(), null, !1, !1);
  }), mt.xlinkHref = new Et("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1), ["src", "href", "action", "formAction"].forEach(function(n) {
    mt[n] = new Et(n, 1, !1, n.toLowerCase(), null, !0, !0);
  });
  function Ke(n, r, l, o) {
    var c = mt.hasOwnProperty(r) ? mt[r] : null;
    (c !== null ? c.type !== 0 : o || !(2 < r.length) || r[0] !== "o" && r[0] !== "O" || r[1] !== "n" && r[1] !== "N") && (qe(r, l, c, o) && (l = null), o || c === null ? me(r) && (l === null ? n.removeAttribute(r) : n.setAttribute(r, "" + l)) : c.mustUseProperty ? n[c.propertyName] = l === null ? c.type === 3 ? !1 : "" : l : (r = c.attributeName, o = c.attributeNamespace, l === null ? n.removeAttribute(r) : (c = c.type, l = c === 3 || c === 4 && l === !0 ? "" : "" + l, o ? n.setAttributeNS(o, r, l) : n.setAttribute(r, l))));
  }
  var yt = O.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, De = Symbol.for("react.element"), dt = Symbol.for("react.portal"), Be = Symbol.for("react.fragment"), ln = Symbol.for("react.strict_mode"), Vt = Symbol.for("react.profiler"), Jt = Symbol.for("react.provider"), un = Symbol.for("react.context"), kt = Symbol.for("react.forward_ref"), Le = Symbol.for("react.suspense"), Ft = Symbol.for("react.suspense_list"), Dt = Symbol.for("react.memo"), Nt = Symbol.for("react.lazy"), Re = Symbol.for("react.offscreen"), J = Symbol.iterator;
  function Te(n) {
    return n === null || typeof n != "object" ? null : (n = J && n[J] || n["@@iterator"], typeof n == "function" ? n : null);
  }
  var ie = Object.assign, k;
  function B(n) {
    if (k === void 0) try {
      throw Error();
    } catch (l) {
      var r = l.stack.trim().match(/\n( *(at )?)/);
      k = r && r[1] || "";
    }
    return `
` + k + n;
  }
  var $e = !1;
  function Fe(n, r) {
    if (!n || $e) return "";
    $e = !0;
    var l = Error.prepareStackTrace;
    Error.prepareStackTrace = void 0;
    try {
      if (r) if (r = function() {
        throw Error();
      }, Object.defineProperty(r.prototype, "props", { set: function() {
        throw Error();
      } }), typeof Reflect == "object" && Reflect.construct) {
        try {
          Reflect.construct(r, []);
        } catch (j) {
          var o = j;
        }
        Reflect.construct(n, [], r);
      } else {
        try {
          r.call();
        } catch (j) {
          o = j;
        }
        n.call(r.prototype);
      }
      else {
        try {
          throw Error();
        } catch (j) {
          o = j;
        }
        n();
      }
    } catch (j) {
      if (j && o && typeof j.stack == "string") {
        for (var c = j.stack.split(`
`), d = o.stack.split(`
`), m = c.length - 1, E = d.length - 1; 1 <= m && 0 <= E && c[m] !== d[E]; ) E--;
        for (; 1 <= m && 0 <= E; m--, E--) if (c[m] !== d[E]) {
          if (m !== 1 || E !== 1)
            do
              if (m--, E--, 0 > E || c[m] !== d[E]) {
                var R = `
` + c[m].replace(" at new ", " at ");
                return n.displayName && R.includes("<anonymous>") && (R = R.replace("<anonymous>", n.displayName)), R;
              }
            while (1 <= m && 0 <= E);
          break;
        }
      }
    } finally {
      $e = !1, Error.prepareStackTrace = l;
    }
    return (n = n ? n.displayName || n.name : "") ? B(n) : "";
  }
  function ut(n) {
    switch (n.tag) {
      case 5:
        return B(n.type);
      case 16:
        return B("Lazy");
      case 13:
        return B("Suspense");
      case 19:
        return B("SuspenseList");
      case 0:
      case 2:
      case 15:
        return n = Fe(n.type, !1), n;
      case 11:
        return n = Fe(n.type.render, !1), n;
      case 1:
        return n = Fe(n.type, !0), n;
      default:
        return "";
    }
  }
  function rt(n) {
    if (n == null) return null;
    if (typeof n == "function") return n.displayName || n.name || null;
    if (typeof n == "string") return n;
    switch (n) {
      case Be:
        return "Fragment";
      case dt:
        return "Portal";
      case Vt:
        return "Profiler";
      case ln:
        return "StrictMode";
      case Le:
        return "Suspense";
      case Ft:
        return "SuspenseList";
    }
    if (typeof n == "object") switch (n.$$typeof) {
      case un:
        return (n.displayName || "Context") + ".Consumer";
      case Jt:
        return (n._context.displayName || "Context") + ".Provider";
      case kt:
        var r = n.render;
        return n = n.displayName, n || (n = r.displayName || r.name || "", n = n !== "" ? "ForwardRef(" + n + ")" : "ForwardRef"), n;
      case Dt:
        return r = n.displayName || null, r !== null ? r : rt(n.type) || "Memo";
      case Nt:
        r = n._payload, n = n._init;
        try {
          return rt(n(r));
        } catch {
        }
    }
    return null;
  }
  function tt(n) {
    var r = n.type;
    switch (n.tag) {
      case 24:
        return "Cache";
      case 9:
        return (r.displayName || "Context") + ".Consumer";
      case 10:
        return (r._context.displayName || "Context") + ".Provider";
      case 18:
        return "DehydratedFragment";
      case 11:
        return n = r.render, n = n.displayName || n.name || "", r.displayName || (n !== "" ? "ForwardRef(" + n + ")" : "ForwardRef");
      case 7:
        return "Fragment";
      case 5:
        return r;
      case 4:
        return "Portal";
      case 3:
        return "Root";
      case 6:
        return "Text";
      case 16:
        return rt(r);
      case 8:
        return r === ln ? "StrictMode" : "Mode";
      case 22:
        return "Offscreen";
      case 12:
        return "Profiler";
      case 21:
        return "Scope";
      case 13:
        return "Suspense";
      case 19:
        return "SuspenseList";
      case 25:
        return "TracingMarker";
      case 1:
      case 0:
      case 17:
      case 2:
      case 14:
      case 15:
        if (typeof r == "function") return r.displayName || r.name || null;
        if (typeof r == "string") return r;
    }
    return null;
  }
  function at(n) {
    switch (typeof n) {
      case "boolean":
      case "number":
      case "string":
      case "undefined":
        return n;
      case "object":
        return n;
      default:
        return "";
    }
  }
  function ot(n) {
    var r = n.type;
    return (n = n.nodeName) && n.toLowerCase() === "input" && (r === "checkbox" || r === "radio");
  }
  function $t(n) {
    var r = ot(n) ? "checked" : "value", l = Object.getOwnPropertyDescriptor(n.constructor.prototype, r), o = "" + n[r];
    if (!n.hasOwnProperty(r) && typeof l < "u" && typeof l.get == "function" && typeof l.set == "function") {
      var c = l.get, d = l.set;
      return Object.defineProperty(n, r, { configurable: !0, get: function() {
        return c.call(this);
      }, set: function(m) {
        o = "" + m, d.call(this, m);
      } }), Object.defineProperty(n, r, { enumerable: l.enumerable }), { getValue: function() {
        return o;
      }, setValue: function(m) {
        o = "" + m;
      }, stopTracking: function() {
        n._valueTracker = null, delete n[r];
      } };
    }
  }
  function Nn(n) {
    n._valueTracker || (n._valueTracker = $t(n));
  }
  function xr(n) {
    if (!n) return !1;
    var r = n._valueTracker;
    if (!r) return !0;
    var l = r.getValue(), o = "";
    return n && (o = ot(n) ? n.checked ? "true" : "false" : n.value), n = o, n !== l ? (r.setValue(n), !0) : !1;
  }
  function _n(n) {
    if (n = n || (typeof document < "u" ? document : void 0), typeof n > "u") return null;
    try {
      return n.activeElement || n.body;
    } catch {
      return n.body;
    }
  }
  function ar(n, r) {
    var l = r.checked;
    return ie({}, r, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: l ?? n._wrapperState.initialChecked });
  }
  function $n(n, r) {
    var l = r.defaultValue == null ? "" : r.defaultValue, o = r.checked != null ? r.checked : r.defaultChecked;
    l = at(r.value != null ? r.value : l), n._wrapperState = { initialChecked: o, initialValue: l, controlled: r.type === "checkbox" || r.type === "radio" ? r.checked != null : r.value != null };
  }
  function In(n, r) {
    r = r.checked, r != null && Ke(n, "checked", r, !1);
  }
  function Wr(n, r) {
    In(n, r);
    var l = at(r.value), o = r.type;
    if (l != null) o === "number" ? (l === 0 && n.value === "" || n.value != l) && (n.value = "" + l) : n.value !== "" + l && (n.value = "" + l);
    else if (o === "submit" || o === "reset") {
      n.removeAttribute("value");
      return;
    }
    r.hasOwnProperty("value") ? fa(n, r.type, l) : r.hasOwnProperty("defaultValue") && fa(n, r.type, at(r.defaultValue)), r.checked == null && r.defaultChecked != null && (n.defaultChecked = !!r.defaultChecked);
  }
  function vi(n, r, l) {
    if (r.hasOwnProperty("value") || r.hasOwnProperty("defaultValue")) {
      var o = r.type;
      if (!(o !== "submit" && o !== "reset" || r.value !== void 0 && r.value !== null)) return;
      r = "" + n._wrapperState.initialValue, l || r === n.value || (n.value = r), n.defaultValue = r;
    }
    l = n.name, l !== "" && (n.name = ""), n.defaultChecked = !!n._wrapperState.initialChecked, l !== "" && (n.name = l);
  }
  function fa(n, r, l) {
    (r !== "number" || _n(n.ownerDocument) !== n) && (l == null ? n.defaultValue = "" + n._wrapperState.initialValue : n.defaultValue !== "" + l && (n.defaultValue = "" + l));
  }
  var Xn = Array.isArray;
  function Rn(n, r, l, o) {
    if (n = n.options, r) {
      r = {};
      for (var c = 0; c < l.length; c++) r["$" + l[c]] = !0;
      for (l = 0; l < n.length; l++) c = r.hasOwnProperty("$" + n[l].value), n[l].selected !== c && (n[l].selected = c), c && o && (n[l].defaultSelected = !0);
    } else {
      for (l = "" + at(l), r = null, c = 0; c < n.length; c++) {
        if (n[c].value === l) {
          n[c].selected = !0, o && (n[c].defaultSelected = !0);
          return;
        }
        r !== null || n[c].disabled || (r = n[c]);
      }
      r !== null && (r.selected = !0);
    }
  }
  function Yn(n, r) {
    if (r.dangerouslySetInnerHTML != null) throw Error(T(91));
    return ie({}, r, { value: void 0, defaultValue: void 0, children: "" + n._wrapperState.initialValue });
  }
  function Er(n, r) {
    var l = r.value;
    if (l == null) {
      if (l = r.children, r = r.defaultValue, l != null) {
        if (r != null) throw Error(T(92));
        if (Xn(l)) {
          if (1 < l.length) throw Error(T(93));
          l = l[0];
        }
        r = l;
      }
      r == null && (r = ""), l = r;
    }
    n._wrapperState = { initialValue: at(l) };
  }
  function qa(n, r) {
    var l = at(r.value), o = at(r.defaultValue);
    l != null && (l = "" + l, l !== n.value && (n.value = l), r.defaultValue == null && n.defaultValue !== l && (n.defaultValue = l)), o != null && (n.defaultValue = "" + o);
  }
  function Ln(n) {
    var r = n.textContent;
    r === n._wrapperState.initialValue && r !== "" && r !== null && (n.value = r);
  }
  function Cr(n) {
    switch (n) {
      case "svg":
        return "http://www.w3.org/2000/svg";
      case "math":
        return "http://www.w3.org/1998/Math/MathML";
      default:
        return "http://www.w3.org/1999/xhtml";
    }
  }
  function da(n, r) {
    return n == null || n === "http://www.w3.org/1999/xhtml" ? Cr(r) : n === "http://www.w3.org/2000/svg" && r === "foreignObject" ? "http://www.w3.org/1999/xhtml" : n;
  }
  var Ka, hi = function(n) {
    return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(r, l, o, c) {
      MSApp.execUnsafeLocalFunction(function() {
        return n(r, l, o, c);
      });
    } : n;
  }(function(n, r) {
    if (n.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in n) n.innerHTML = r;
    else {
      for (Ka = Ka || document.createElement("div"), Ka.innerHTML = "<svg>" + r.valueOf().toString() + "</svg>", r = Ka.firstChild; n.firstChild; ) n.removeChild(n.firstChild);
      for (; r.firstChild; ) n.appendChild(r.firstChild);
    }
  });
  function re(n, r) {
    if (r) {
      var l = n.firstChild;
      if (l && l === n.lastChild && l.nodeType === 3) {
        l.nodeValue = r;
        return;
      }
    }
    n.textContent = r;
  }
  var be = {
    animationIterationCount: !0,
    aspectRatio: !0,
    borderImageOutset: !0,
    borderImageSlice: !0,
    borderImageWidth: !0,
    boxFlex: !0,
    boxFlexGroup: !0,
    boxOrdinalGroup: !0,
    columnCount: !0,
    columns: !0,
    flex: !0,
    flexGrow: !0,
    flexPositive: !0,
    flexShrink: !0,
    flexNegative: !0,
    flexOrder: !0,
    gridArea: !0,
    gridRow: !0,
    gridRowEnd: !0,
    gridRowSpan: !0,
    gridRowStart: !0,
    gridColumn: !0,
    gridColumnEnd: !0,
    gridColumnSpan: !0,
    gridColumnStart: !0,
    fontWeight: !0,
    lineClamp: !0,
    lineHeight: !0,
    opacity: !0,
    order: !0,
    orphans: !0,
    tabSize: !0,
    widows: !0,
    zIndex: !0,
    zoom: !0,
    fillOpacity: !0,
    floodOpacity: !0,
    stopOpacity: !0,
    strokeDasharray: !0,
    strokeDashoffset: !0,
    strokeMiterlimit: !0,
    strokeOpacity: !0,
    strokeWidth: !0
  }, it = ["Webkit", "ms", "Moz", "O"];
  Object.keys(be).forEach(function(n) {
    it.forEach(function(r) {
      r = r + n.charAt(0).toUpperCase() + n.substring(1), be[r] = be[n];
    });
  });
  function Ht(n, r, l) {
    return r == null || typeof r == "boolean" || r === "" ? "" : l || typeof r != "number" || r === 0 || be.hasOwnProperty(n) && be[n] ? ("" + r).trim() : r + "px";
  }
  function en(n, r) {
    n = n.style;
    for (var l in r) if (r.hasOwnProperty(l)) {
      var o = l.indexOf("--") === 0, c = Ht(l, r[l], o);
      l === "float" && (l = "cssFloat"), o ? n.setProperty(l, c) : n[l] = c;
    }
  }
  var hn = ie({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
  function on(n, r) {
    if (r) {
      if (hn[n] && (r.children != null || r.dangerouslySetInnerHTML != null)) throw Error(T(137, n));
      if (r.dangerouslySetInnerHTML != null) {
        if (r.children != null) throw Error(T(60));
        if (typeof r.dangerouslySetInnerHTML != "object" || !("__html" in r.dangerouslySetInnerHTML)) throw Error(T(61));
      }
      if (r.style != null && typeof r.style != "object") throw Error(T(62));
    }
  }
  function Zn(n, r) {
    if (n.indexOf("-") === -1) return typeof r.is == "string";
    switch (n) {
      case "annotation-xml":
      case "color-profile":
      case "font-face":
      case "font-face-src":
      case "font-face-uri":
      case "font-face-format":
      case "font-face-name":
      case "missing-glyph":
        return !1;
      default:
        return !0;
    }
  }
  var tn = null;
  function It(n) {
    return n = n.target || n.srcElement || window, n.correspondingUseElement && (n = n.correspondingUseElement), n.nodeType === 3 ? n.parentNode : n;
  }
  var Yt = null, pa = null, _r = null;
  function xa(n) {
    if (n = Oe(n)) {
      if (typeof Yt != "function") throw Error(T(280));
      var r = n.stateNode;
      r && (r = yn(r), Yt(n.stateNode, n.type, r));
    }
  }
  function $i(n) {
    pa ? _r ? _r.push(n) : _r = [n] : pa = n;
  }
  function lu() {
    if (pa) {
      var n = pa, r = _r;
      if (_r = pa = null, xa(n), r) for (n = 0; n < r.length; n++) xa(r[n]);
    }
  }
  function uu(n, r) {
    return n(r);
  }
  function El() {
  }
  var Cl = !1;
  function ou(n, r, l) {
    if (Cl) return n(r, l);
    Cl = !0;
    try {
      return uu(n, r, l);
    } finally {
      Cl = !1, (pa !== null || _r !== null) && (El(), lu());
    }
  }
  function kr(n, r) {
    var l = n.stateNode;
    if (l === null) return null;
    var o = yn(l);
    if (o === null) return null;
    l = o[r];
    e: switch (r) {
      case "onClick":
      case "onClickCapture":
      case "onDoubleClick":
      case "onDoubleClickCapture":
      case "onMouseDown":
      case "onMouseDownCapture":
      case "onMouseMove":
      case "onMouseMoveCapture":
      case "onMouseUp":
      case "onMouseUpCapture":
      case "onMouseEnter":
        (o = !o.disabled) || (n = n.type, o = !(n === "button" || n === "input" || n === "select" || n === "textarea")), n = !o;
        break e;
      default:
        n = !1;
    }
    if (n) return null;
    if (l && typeof l != "function") throw Error(T(231, r, typeof l));
    return l;
  }
  var Dr = !1;
  if (ft) try {
    var ir = {};
    Object.defineProperty(ir, "passive", { get: function() {
      Dr = !0;
    } }), window.addEventListener("test", ir, ir), window.removeEventListener("test", ir, ir);
  } catch {
    Dr = !1;
  }
  function mi(n, r, l, o, c, d, m, E, R) {
    var j = Array.prototype.slice.call(arguments, 3);
    try {
      r.apply(l, j);
    } catch (W) {
      this.onError(W);
    }
  }
  var Xa = !1, yi = null, gi = !1, _ = null, I = { onError: function(n) {
    Xa = !0, yi = n;
  } };
  function ue(n, r, l, o, c, d, m, E, R) {
    Xa = !1, yi = null, mi.apply(I, arguments);
  }
  function ge(n, r, l, o, c, d, m, E, R) {
    if (ue.apply(this, arguments), Xa) {
      if (Xa) {
        var j = yi;
        Xa = !1, yi = null;
      } else throw Error(T(198));
      gi || (gi = !0, _ = j);
    }
  }
  function Ze(n) {
    var r = n, l = n;
    if (n.alternate) for (; r.return; ) r = r.return;
    else {
      n = r;
      do
        r = n, r.flags & 4098 && (l = r.return), n = r.return;
      while (n);
    }
    return r.tag === 3 ? l : null;
  }
  function We(n) {
    if (n.tag === 13) {
      var r = n.memoizedState;
      if (r === null && (n = n.alternate, n !== null && (r = n.memoizedState)), r !== null) return r.dehydrated;
    }
    return null;
  }
  function pt(n) {
    if (Ze(n) !== n) throw Error(T(188));
  }
  function st(n) {
    var r = n.alternate;
    if (!r) {
      if (r = Ze(n), r === null) throw Error(T(188));
      return r !== n ? null : n;
    }
    for (var l = n, o = r; ; ) {
      var c = l.return;
      if (c === null) break;
      var d = c.alternate;
      if (d === null) {
        if (o = c.return, o !== null) {
          l = o;
          continue;
        }
        break;
      }
      if (c.child === d.child) {
        for (d = c.child; d; ) {
          if (d === l) return pt(c), n;
          if (d === o) return pt(c), r;
          d = d.sibling;
        }
        throw Error(T(188));
      }
      if (l.return !== o.return) l = c, o = d;
      else {
        for (var m = !1, E = c.child; E; ) {
          if (E === l) {
            m = !0, l = c, o = d;
            break;
          }
          if (E === o) {
            m = !0, o = c, l = d;
            break;
          }
          E = E.sibling;
        }
        if (!m) {
          for (E = d.child; E; ) {
            if (E === l) {
              m = !0, l = d, o = c;
              break;
            }
            if (E === o) {
              m = !0, o = d, l = c;
              break;
            }
            E = E.sibling;
          }
          if (!m) throw Error(T(189));
        }
      }
      if (l.alternate !== o) throw Error(T(190));
    }
    if (l.tag !== 3) throw Error(T(188));
    return l.stateNode.current === l ? n : r;
  }
  function Tn(n) {
    return n = st(n), n !== null ? nn(n) : null;
  }
  function nn(n) {
    if (n.tag === 5 || n.tag === 6) return n;
    for (n = n.child; n !== null; ) {
      var r = nn(n);
      if (r !== null) return r;
      n = n.sibling;
    }
    return null;
  }
  var sn = A.unstable_scheduleCallback, lr = A.unstable_cancelCallback, Za = A.unstable_shouldYield, Ja = A.unstable_requestPaint, Je = A.unstable_now, nt = A.unstable_getCurrentPriorityLevel, ei = A.unstable_ImmediatePriority, su = A.unstable_UserBlockingPriority, cu = A.unstable_NormalPriority, _l = A.unstable_LowPriority, eo = A.unstable_IdlePriority, Rl = null, Gr = null;
  function Zo(n) {
    if (Gr && typeof Gr.onCommitFiberRoot == "function") try {
      Gr.onCommitFiberRoot(Rl, n, void 0, (n.current.flags & 128) === 128);
    } catch {
    }
  }
  var Or = Math.clz32 ? Math.clz32 : to, pc = Math.log, vc = Math.LN2;
  function to(n) {
    return n >>>= 0, n === 0 ? 32 : 31 - (pc(n) / vc | 0) | 0;
  }
  var Tl = 64, va = 4194304;
  function ti(n) {
    switch (n & -n) {
      case 1:
        return 1;
      case 2:
        return 2;
      case 4:
        return 4;
      case 8:
        return 8;
      case 16:
        return 16;
      case 32:
        return 32;
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return n & 4194240;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return n & 130023424;
      case 134217728:
        return 134217728;
      case 268435456:
        return 268435456;
      case 536870912:
        return 536870912;
      case 1073741824:
        return 1073741824;
      default:
        return n;
    }
  }
  function ni(n, r) {
    var l = n.pendingLanes;
    if (l === 0) return 0;
    var o = 0, c = n.suspendedLanes, d = n.pingedLanes, m = l & 268435455;
    if (m !== 0) {
      var E = m & ~c;
      E !== 0 ? o = ti(E) : (d &= m, d !== 0 && (o = ti(d)));
    } else m = l & ~c, m !== 0 ? o = ti(m) : d !== 0 && (o = ti(d));
    if (o === 0) return 0;
    if (r !== 0 && r !== o && !(r & c) && (c = o & -o, d = r & -r, c >= d || c === 16 && (d & 4194240) !== 0)) return r;
    if (o & 4 && (o |= l & 16), r = n.entangledLanes, r !== 0) for (n = n.entanglements, r &= o; 0 < r; ) l = 31 - Or(r), c = 1 << l, o |= n[l], r &= ~c;
    return o;
  }
  function no(n, r) {
    switch (n) {
      case 1:
      case 2:
      case 4:
        return r + 250;
      case 8:
      case 16:
      case 32:
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return r + 5e3;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return -1;
      case 134217728:
      case 268435456:
      case 536870912:
      case 1073741824:
        return -1;
      default:
        return -1;
    }
  }
  function fu(n, r) {
    for (var l = n.suspendedLanes, o = n.pingedLanes, c = n.expirationTimes, d = n.pendingLanes; 0 < d; ) {
      var m = 31 - Or(d), E = 1 << m, R = c[m];
      R === -1 ? (!(E & l) || E & o) && (c[m] = no(E, r)) : R <= r && (n.expiredLanes |= E), d &= ~E;
    }
  }
  function bl(n) {
    return n = n.pendingLanes & -1073741825, n !== 0 ? n : n & 1073741824 ? 1073741824 : 0;
  }
  function ro() {
    var n = Tl;
    return Tl <<= 1, !(Tl & 4194240) && (Tl = 64), n;
  }
  function ao(n) {
    for (var r = [], l = 0; 31 > l; l++) r.push(n);
    return r;
  }
  function Ii(n, r, l) {
    n.pendingLanes |= r, r !== 536870912 && (n.suspendedLanes = 0, n.pingedLanes = 0), n = n.eventTimes, r = 31 - Or(r), n[r] = l;
  }
  function Jf(n, r) {
    var l = n.pendingLanes & ~r;
    n.pendingLanes = r, n.suspendedLanes = 0, n.pingedLanes = 0, n.expiredLanes &= r, n.mutableReadLanes &= r, n.entangledLanes &= r, r = n.entanglements;
    var o = n.eventTimes;
    for (n = n.expirationTimes; 0 < l; ) {
      var c = 31 - Or(l), d = 1 << c;
      r[c] = 0, o[c] = -1, n[c] = -1, l &= ~d;
    }
  }
  function Yi(n, r) {
    var l = n.entangledLanes |= r;
    for (n = n.entanglements; l; ) {
      var o = 31 - Or(l), c = 1 << o;
      c & r | n[o] & r && (n[o] |= r), l &= ~c;
    }
  }
  var Lt = 0;
  function io(n) {
    return n &= -n, 1 < n ? 4 < n ? n & 268435455 ? 16 : 536870912 : 4 : 1;
  }
  var wt, Jo, Si, Qe, lo, ur = !1, Ei = [], Nr = null, Ci = null, cn = null, Qt = /* @__PURE__ */ new Map(), wl = /* @__PURE__ */ new Map(), Qn = [], Lr = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
  function ka(n, r) {
    switch (n) {
      case "focusin":
      case "focusout":
        Nr = null;
        break;
      case "dragenter":
      case "dragleave":
        Ci = null;
        break;
      case "mouseover":
      case "mouseout":
        cn = null;
        break;
      case "pointerover":
      case "pointerout":
        Qt.delete(r.pointerId);
        break;
      case "gotpointercapture":
      case "lostpointercapture":
        wl.delete(r.pointerId);
    }
  }
  function du(n, r, l, o, c, d) {
    return n === null || n.nativeEvent !== d ? (n = { blockedOn: r, domEventName: l, eventSystemFlags: o, nativeEvent: d, targetContainers: [c] }, r !== null && (r = Oe(r), r !== null && Jo(r)), n) : (n.eventSystemFlags |= o, r = n.targetContainers, c !== null && r.indexOf(c) === -1 && r.push(c), n);
  }
  function es(n, r, l, o, c) {
    switch (r) {
      case "focusin":
        return Nr = du(Nr, n, r, l, o, c), !0;
      case "dragenter":
        return Ci = du(Ci, n, r, l, o, c), !0;
      case "mouseover":
        return cn = du(cn, n, r, l, o, c), !0;
      case "pointerover":
        var d = c.pointerId;
        return Qt.set(d, du(Qt.get(d) || null, n, r, l, o, c)), !0;
      case "gotpointercapture":
        return d = c.pointerId, wl.set(d, du(wl.get(d) || null, n, r, l, o, c)), !0;
    }
    return !1;
  }
  function ts(n) {
    var r = Cu(n.target);
    if (r !== null) {
      var l = Ze(r);
      if (l !== null) {
        if (r = l.tag, r === 13) {
          if (r = We(l), r !== null) {
            n.blockedOn = r, lo(n.priority, function() {
              Si(l);
            });
            return;
          }
        } else if (r === 3 && l.stateNode.current.memoizedState.isDehydrated) {
          n.blockedOn = l.tag === 3 ? l.stateNode.containerInfo : null;
          return;
        }
      }
    }
    n.blockedOn = null;
  }
  function xl(n) {
    if (n.blockedOn !== null) return !1;
    for (var r = n.targetContainers; 0 < r.length; ) {
      var l = so(n.domEventName, n.eventSystemFlags, r[0], n.nativeEvent);
      if (l === null) {
        l = n.nativeEvent;
        var o = new l.constructor(l.type, l);
        tn = o, l.target.dispatchEvent(o), tn = null;
      } else return r = Oe(l), r !== null && Jo(r), n.blockedOn = l, !1;
      r.shift();
    }
    return !0;
  }
  function pu(n, r, l) {
    xl(n) && l.delete(r);
  }
  function ed() {
    ur = !1, Nr !== null && xl(Nr) && (Nr = null), Ci !== null && xl(Ci) && (Ci = null), cn !== null && xl(cn) && (cn = null), Qt.forEach(pu), wl.forEach(pu);
  }
  function Da(n, r) {
    n.blockedOn === r && (n.blockedOn = null, ur || (ur = !0, A.unstable_scheduleCallback(A.unstable_NormalPriority, ed)));
  }
  function ri(n) {
    function r(c) {
      return Da(c, n);
    }
    if (0 < Ei.length) {
      Da(Ei[0], n);
      for (var l = 1; l < Ei.length; l++) {
        var o = Ei[l];
        o.blockedOn === n && (o.blockedOn = null);
      }
    }
    for (Nr !== null && Da(Nr, n), Ci !== null && Da(Ci, n), cn !== null && Da(cn, n), Qt.forEach(r), wl.forEach(r), l = 0; l < Qn.length; l++) o = Qn[l], o.blockedOn === n && (o.blockedOn = null);
    for (; 0 < Qn.length && (l = Qn[0], l.blockedOn === null); ) ts(l), l.blockedOn === null && Qn.shift();
  }
  var _i = yt.ReactCurrentBatchConfig, Oa = !0;
  function uo(n, r, l, o) {
    var c = Lt, d = _i.transition;
    _i.transition = null;
    try {
      Lt = 1, kl(n, r, l, o);
    } finally {
      Lt = c, _i.transition = d;
    }
  }
  function oo(n, r, l, o) {
    var c = Lt, d = _i.transition;
    _i.transition = null;
    try {
      Lt = 4, kl(n, r, l, o);
    } finally {
      Lt = c, _i.transition = d;
    }
  }
  function kl(n, r, l, o) {
    if (Oa) {
      var c = so(n, r, l, o);
      if (c === null) wc(n, r, o, vu, l), ka(n, o);
      else if (es(c, n, r, l, o)) o.stopPropagation();
      else if (ka(n, o), r & 4 && -1 < Lr.indexOf(n)) {
        for (; c !== null; ) {
          var d = Oe(c);
          if (d !== null && wt(d), d = so(n, r, l, o), d === null && wc(n, r, o, vu, l), d === c) break;
          c = d;
        }
        c !== null && o.stopPropagation();
      } else wc(n, r, o, null, l);
    }
  }
  var vu = null;
  function so(n, r, l, o) {
    if (vu = null, n = It(o), n = Cu(n), n !== null) if (r = Ze(n), r === null) n = null;
    else if (l = r.tag, l === 13) {
      if (n = We(r), n !== null) return n;
      n = null;
    } else if (l === 3) {
      if (r.stateNode.current.memoizedState.isDehydrated) return r.tag === 3 ? r.stateNode.containerInfo : null;
      n = null;
    } else r !== n && (n = null);
    return vu = n, null;
  }
  function co(n) {
    switch (n) {
      case "cancel":
      case "click":
      case "close":
      case "contextmenu":
      case "copy":
      case "cut":
      case "auxclick":
      case "dblclick":
      case "dragend":
      case "dragstart":
      case "drop":
      case "focusin":
      case "focusout":
      case "input":
      case "invalid":
      case "keydown":
      case "keypress":
      case "keyup":
      case "mousedown":
      case "mouseup":
      case "paste":
      case "pause":
      case "play":
      case "pointercancel":
      case "pointerdown":
      case "pointerup":
      case "ratechange":
      case "reset":
      case "resize":
      case "seeked":
      case "submit":
      case "touchcancel":
      case "touchend":
      case "touchstart":
      case "volumechange":
      case "change":
      case "selectionchange":
      case "textInput":
      case "compositionstart":
      case "compositionend":
      case "compositionupdate":
      case "beforeblur":
      case "afterblur":
      case "beforeinput":
      case "blur":
      case "fullscreenchange":
      case "focus":
      case "hashchange":
      case "popstate":
      case "select":
      case "selectstart":
        return 1;
      case "drag":
      case "dragenter":
      case "dragexit":
      case "dragleave":
      case "dragover":
      case "mousemove":
      case "mouseout":
      case "mouseover":
      case "pointermove":
      case "pointerout":
      case "pointerover":
      case "scroll":
      case "toggle":
      case "touchmove":
      case "wheel":
      case "mouseenter":
      case "mouseleave":
      case "pointerenter":
      case "pointerleave":
        return 4;
      case "message":
        switch (nt()) {
          case ei:
            return 1;
          case su:
            return 4;
          case cu:
          case _l:
            return 16;
          case eo:
            return 536870912;
          default:
            return 16;
        }
      default:
        return 16;
    }
  }
  var ai = null, h = null, C = null;
  function z() {
    if (C) return C;
    var n, r = h, l = r.length, o, c = "value" in ai ? ai.value : ai.textContent, d = c.length;
    for (n = 0; n < l && r[n] === c[n]; n++) ;
    var m = l - n;
    for (o = 1; o <= m && r[l - o] === c[d - o]; o++) ;
    return C = c.slice(n, 1 < o ? 1 - o : void 0);
  }
  function H(n) {
    var r = n.keyCode;
    return "charCode" in n ? (n = n.charCode, n === 0 && r === 13 && (n = 13)) : n = r, n === 10 && (n = 13), 32 <= n || n === 13 ? n : 0;
  }
  function Z() {
    return !0;
  }
  function Me() {
    return !1;
  }
  function le(n) {
    function r(l, o, c, d, m) {
      this._reactName = l, this._targetInst = c, this.type = o, this.nativeEvent = d, this.target = m, this.currentTarget = null;
      for (var E in n) n.hasOwnProperty(E) && (l = n[E], this[E] = l ? l(d) : d[E]);
      return this.isDefaultPrevented = (d.defaultPrevented != null ? d.defaultPrevented : d.returnValue === !1) ? Z : Me, this.isPropagationStopped = Me, this;
    }
    return ie(r.prototype, { preventDefault: function() {
      this.defaultPrevented = !0;
      var l = this.nativeEvent;
      l && (l.preventDefault ? l.preventDefault() : typeof l.returnValue != "unknown" && (l.returnValue = !1), this.isDefaultPrevented = Z);
    }, stopPropagation: function() {
      var l = this.nativeEvent;
      l && (l.stopPropagation ? l.stopPropagation() : typeof l.cancelBubble != "unknown" && (l.cancelBubble = !0), this.isPropagationStopped = Z);
    }, persist: function() {
    }, isPersistent: Z }), r;
  }
  var Ae = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(n) {
    return n.timeStamp || Date.now();
  }, defaultPrevented: 0, isTrusted: 0 }, vt = le(Ae), xt = ie({}, Ae, { view: 0, detail: 0 }), rn = le(xt), Wt, lt, Gt, mn = ie({}, xt, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: id, button: 0, buttons: 0, relatedTarget: function(n) {
    return n.relatedTarget === void 0 ? n.fromElement === n.srcElement ? n.toElement : n.fromElement : n.relatedTarget;
  }, movementX: function(n) {
    return "movementX" in n ? n.movementX : (n !== Gt && (Gt && n.type === "mousemove" ? (Wt = n.screenX - Gt.screenX, lt = n.screenY - Gt.screenY) : lt = Wt = 0, Gt = n), Wt);
  }, movementY: function(n) {
    return "movementY" in n ? n.movementY : lt;
  } }), Dl = le(mn), ns = ie({}, mn, { dataTransfer: 0 }), Qi = le(ns), rs = ie({}, xt, { relatedTarget: 0 }), hu = le(rs), td = ie({}, Ae, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), hc = le(td), nd = ie({}, Ae, { clipboardData: function(n) {
    return "clipboardData" in n ? n.clipboardData : window.clipboardData;
  } }), ov = le(nd), rd = ie({}, Ae, { data: 0 }), ad = le(rd), sv = {
    Esc: "Escape",
    Spacebar: " ",
    Left: "ArrowLeft",
    Up: "ArrowUp",
    Right: "ArrowRight",
    Down: "ArrowDown",
    Del: "Delete",
    Win: "OS",
    Menu: "ContextMenu",
    Apps: "ContextMenu",
    Scroll: "ScrollLock",
    MozPrintableKey: "Unidentified"
  }, cv = {
    8: "Backspace",
    9: "Tab",
    12: "Clear",
    13: "Enter",
    16: "Shift",
    17: "Control",
    18: "Alt",
    19: "Pause",
    20: "CapsLock",
    27: "Escape",
    32: " ",
    33: "PageUp",
    34: "PageDown",
    35: "End",
    36: "Home",
    37: "ArrowLeft",
    38: "ArrowUp",
    39: "ArrowRight",
    40: "ArrowDown",
    45: "Insert",
    46: "Delete",
    112: "F1",
    113: "F2",
    114: "F3",
    115: "F4",
    116: "F5",
    117: "F6",
    118: "F7",
    119: "F8",
    120: "F9",
    121: "F10",
    122: "F11",
    123: "F12",
    144: "NumLock",
    145: "ScrollLock",
    224: "Meta"
  }, ay = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
  function Wi(n) {
    var r = this.nativeEvent;
    return r.getModifierState ? r.getModifierState(n) : (n = ay[n]) ? !!r[n] : !1;
  }
  function id() {
    return Wi;
  }
  var ld = ie({}, xt, { key: function(n) {
    if (n.key) {
      var r = sv[n.key] || n.key;
      if (r !== "Unidentified") return r;
    }
    return n.type === "keypress" ? (n = H(n), n === 13 ? "Enter" : String.fromCharCode(n)) : n.type === "keydown" || n.type === "keyup" ? cv[n.keyCode] || "Unidentified" : "";
  }, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: id, charCode: function(n) {
    return n.type === "keypress" ? H(n) : 0;
  }, keyCode: function(n) {
    return n.type === "keydown" || n.type === "keyup" ? n.keyCode : 0;
  }, which: function(n) {
    return n.type === "keypress" ? H(n) : n.type === "keydown" || n.type === "keyup" ? n.keyCode : 0;
  } }), ud = le(ld), od = ie({}, mn, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), fv = le(od), mc = ie({}, xt, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: id }), dv = le(mc), qr = ie({}, Ae, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), Gi = le(qr), Mn = ie({}, mn, {
    deltaX: function(n) {
      return "deltaX" in n ? n.deltaX : "wheelDeltaX" in n ? -n.wheelDeltaX : 0;
    },
    deltaY: function(n) {
      return "deltaY" in n ? n.deltaY : "wheelDeltaY" in n ? -n.wheelDeltaY : "wheelDelta" in n ? -n.wheelDelta : 0;
    },
    deltaZ: 0,
    deltaMode: 0
  }), qi = le(Mn), sd = [9, 13, 27, 32], fo = ft && "CompositionEvent" in window, as = null;
  ft && "documentMode" in document && (as = document.documentMode);
  var is = ft && "TextEvent" in window && !as, pv = ft && (!fo || as && 8 < as && 11 >= as), vv = " ", yc = !1;
  function hv(n, r) {
    switch (n) {
      case "keyup":
        return sd.indexOf(r.keyCode) !== -1;
      case "keydown":
        return r.keyCode !== 229;
      case "keypress":
      case "mousedown":
      case "focusout":
        return !0;
      default:
        return !1;
    }
  }
  function mv(n) {
    return n = n.detail, typeof n == "object" && "data" in n ? n.data : null;
  }
  var po = !1;
  function yv(n, r) {
    switch (n) {
      case "compositionend":
        return mv(r);
      case "keypress":
        return r.which !== 32 ? null : (yc = !0, vv);
      case "textInput":
        return n = r.data, n === vv && yc ? null : n;
      default:
        return null;
    }
  }
  function iy(n, r) {
    if (po) return n === "compositionend" || !fo && hv(n, r) ? (n = z(), C = h = ai = null, po = !1, n) : null;
    switch (n) {
      case "paste":
        return null;
      case "keypress":
        if (!(r.ctrlKey || r.altKey || r.metaKey) || r.ctrlKey && r.altKey) {
          if (r.char && 1 < r.char.length) return r.char;
          if (r.which) return String.fromCharCode(r.which);
        }
        return null;
      case "compositionend":
        return pv && r.locale !== "ko" ? null : r.data;
      default:
        return null;
    }
  }
  var ly = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
  function gv(n) {
    var r = n && n.nodeName && n.nodeName.toLowerCase();
    return r === "input" ? !!ly[n.type] : r === "textarea";
  }
  function cd(n, r, l, o) {
    $i(o), r = fs(r, "onChange"), 0 < r.length && (l = new vt("onChange", "change", null, l, o), n.push({ event: l, listeners: r }));
  }
  var Ri = null, mu = null;
  function Sv(n) {
    Su(n, 0);
  }
  function ls(n) {
    var r = li(n);
    if (xr(r)) return n;
  }
  function uy(n, r) {
    if (n === "change") return r;
  }
  var Ev = !1;
  if (ft) {
    var fd;
    if (ft) {
      var dd = "oninput" in document;
      if (!dd) {
        var Cv = document.createElement("div");
        Cv.setAttribute("oninput", "return;"), dd = typeof Cv.oninput == "function";
      }
      fd = dd;
    } else fd = !1;
    Ev = fd && (!document.documentMode || 9 < document.documentMode);
  }
  function _v() {
    Ri && (Ri.detachEvent("onpropertychange", Rv), mu = Ri = null);
  }
  function Rv(n) {
    if (n.propertyName === "value" && ls(mu)) {
      var r = [];
      cd(r, mu, n, It(n)), ou(Sv, r);
    }
  }
  function oy(n, r, l) {
    n === "focusin" ? (_v(), Ri = r, mu = l, Ri.attachEvent("onpropertychange", Rv)) : n === "focusout" && _v();
  }
  function Tv(n) {
    if (n === "selectionchange" || n === "keyup" || n === "keydown") return ls(mu);
  }
  function sy(n, r) {
    if (n === "click") return ls(r);
  }
  function bv(n, r) {
    if (n === "input" || n === "change") return ls(r);
  }
  function cy(n, r) {
    return n === r && (n !== 0 || 1 / n === 1 / r) || n !== n && r !== r;
  }
  var ii = typeof Object.is == "function" ? Object.is : cy;
  function us(n, r) {
    if (ii(n, r)) return !0;
    if (typeof n != "object" || n === null || typeof r != "object" || r === null) return !1;
    var l = Object.keys(n), o = Object.keys(r);
    if (l.length !== o.length) return !1;
    for (o = 0; o < l.length; o++) {
      var c = l[o];
      if (!ee.call(r, c) || !ii(n[c], r[c])) return !1;
    }
    return !0;
  }
  function wv(n) {
    for (; n && n.firstChild; ) n = n.firstChild;
    return n;
  }
  function gc(n, r) {
    var l = wv(n);
    n = 0;
    for (var o; l; ) {
      if (l.nodeType === 3) {
        if (o = n + l.textContent.length, n <= r && o >= r) return { node: l, offset: r - n };
        n = o;
      }
      e: {
        for (; l; ) {
          if (l.nextSibling) {
            l = l.nextSibling;
            break e;
          }
          l = l.parentNode;
        }
        l = void 0;
      }
      l = wv(l);
    }
  }
  function Ol(n, r) {
    return n && r ? n === r ? !0 : n && n.nodeType === 3 ? !1 : r && r.nodeType === 3 ? Ol(n, r.parentNode) : "contains" in n ? n.contains(r) : n.compareDocumentPosition ? !!(n.compareDocumentPosition(r) & 16) : !1 : !1;
  }
  function os() {
    for (var n = window, r = _n(); r instanceof n.HTMLIFrameElement; ) {
      try {
        var l = typeof r.contentWindow.location.href == "string";
      } catch {
        l = !1;
      }
      if (l) n = r.contentWindow;
      else break;
      r = _n(n.document);
    }
    return r;
  }
  function Sc(n) {
    var r = n && n.nodeName && n.nodeName.toLowerCase();
    return r && (r === "input" && (n.type === "text" || n.type === "search" || n.type === "tel" || n.type === "url" || n.type === "password") || r === "textarea" || n.contentEditable === "true");
  }
  function vo(n) {
    var r = os(), l = n.focusedElem, o = n.selectionRange;
    if (r !== l && l && l.ownerDocument && Ol(l.ownerDocument.documentElement, l)) {
      if (o !== null && Sc(l)) {
        if (r = o.start, n = o.end, n === void 0 && (n = r), "selectionStart" in l) l.selectionStart = r, l.selectionEnd = Math.min(n, l.value.length);
        else if (n = (r = l.ownerDocument || document) && r.defaultView || window, n.getSelection) {
          n = n.getSelection();
          var c = l.textContent.length, d = Math.min(o.start, c);
          o = o.end === void 0 ? d : Math.min(o.end, c), !n.extend && d > o && (c = o, o = d, d = c), c = gc(l, d);
          var m = gc(
            l,
            o
          );
          c && m && (n.rangeCount !== 1 || n.anchorNode !== c.node || n.anchorOffset !== c.offset || n.focusNode !== m.node || n.focusOffset !== m.offset) && (r = r.createRange(), r.setStart(c.node, c.offset), n.removeAllRanges(), d > o ? (n.addRange(r), n.extend(m.node, m.offset)) : (r.setEnd(m.node, m.offset), n.addRange(r)));
        }
      }
      for (r = [], n = l; n = n.parentNode; ) n.nodeType === 1 && r.push({ element: n, left: n.scrollLeft, top: n.scrollTop });
      for (typeof l.focus == "function" && l.focus(), l = 0; l < r.length; l++) n = r[l], n.element.scrollLeft = n.left, n.element.scrollTop = n.top;
    }
  }
  var fy = ft && "documentMode" in document && 11 >= document.documentMode, ho = null, pd = null, ss = null, vd = !1;
  function hd(n, r, l) {
    var o = l.window === l ? l.document : l.nodeType === 9 ? l : l.ownerDocument;
    vd || ho == null || ho !== _n(o) || (o = ho, "selectionStart" in o && Sc(o) ? o = { start: o.selectionStart, end: o.selectionEnd } : (o = (o.ownerDocument && o.ownerDocument.defaultView || window).getSelection(), o = { anchorNode: o.anchorNode, anchorOffset: o.anchorOffset, focusNode: o.focusNode, focusOffset: o.focusOffset }), ss && us(ss, o) || (ss = o, o = fs(pd, "onSelect"), 0 < o.length && (r = new vt("onSelect", "select", null, r, l), n.push({ event: r, listeners: o }), r.target = ho)));
  }
  function Ec(n, r) {
    var l = {};
    return l[n.toLowerCase()] = r.toLowerCase(), l["Webkit" + n] = "webkit" + r, l["Moz" + n] = "moz" + r, l;
  }
  var yu = { animationend: Ec("Animation", "AnimationEnd"), animationiteration: Ec("Animation", "AnimationIteration"), animationstart: Ec("Animation", "AnimationStart"), transitionend: Ec("Transition", "TransitionEnd") }, or = {}, md = {};
  ft && (md = document.createElement("div").style, "AnimationEvent" in window || (delete yu.animationend.animation, delete yu.animationiteration.animation, delete yu.animationstart.animation), "TransitionEvent" in window || delete yu.transitionend.transition);
  function Cc(n) {
    if (or[n]) return or[n];
    if (!yu[n]) return n;
    var r = yu[n], l;
    for (l in r) if (r.hasOwnProperty(l) && l in md) return or[n] = r[l];
    return n;
  }
  var xv = Cc("animationend"), kv = Cc("animationiteration"), Dv = Cc("animationstart"), Ov = Cc("transitionend"), yd = /* @__PURE__ */ new Map(), _c = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
  function Na(n, r) {
    yd.set(n, r), He(r, [n]);
  }
  for (var gd = 0; gd < _c.length; gd++) {
    var gu = _c[gd], dy = gu.toLowerCase(), py = gu[0].toUpperCase() + gu.slice(1);
    Na(dy, "on" + py);
  }
  Na(xv, "onAnimationEnd"), Na(kv, "onAnimationIteration"), Na(Dv, "onAnimationStart"), Na("dblclick", "onDoubleClick"), Na("focusin", "onFocus"), Na("focusout", "onBlur"), Na(Ov, "onTransitionEnd"), S("onMouseEnter", ["mouseout", "mouseover"]), S("onMouseLeave", ["mouseout", "mouseover"]), S("onPointerEnter", ["pointerout", "pointerover"]), S("onPointerLeave", ["pointerout", "pointerover"]), He("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" ")), He("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")), He("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]), He("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" ")), He("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" ")), He("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
  var cs = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), Sd = new Set("cancel close invalid load scroll toggle".split(" ").concat(cs));
  function Rc(n, r, l) {
    var o = n.type || "unknown-event";
    n.currentTarget = l, ge(o, r, void 0, n), n.currentTarget = null;
  }
  function Su(n, r) {
    r = (r & 4) !== 0;
    for (var l = 0; l < n.length; l++) {
      var o = n[l], c = o.event;
      o = o.listeners;
      e: {
        var d = void 0;
        if (r) for (var m = o.length - 1; 0 <= m; m--) {
          var E = o[m], R = E.instance, j = E.currentTarget;
          if (E = E.listener, R !== d && c.isPropagationStopped()) break e;
          Rc(c, E, j), d = R;
        }
        else for (m = 0; m < o.length; m++) {
          if (E = o[m], R = E.instance, j = E.currentTarget, E = E.listener, R !== d && c.isPropagationStopped()) break e;
          Rc(c, E, j), d = R;
        }
      }
    }
    if (gi) throw n = _, gi = !1, _ = null, n;
  }
  function Pt(n, r) {
    var l = r[vs];
    l === void 0 && (l = r[vs] = /* @__PURE__ */ new Set());
    var o = n + "__bubble";
    l.has(o) || (Nv(r, n, 2, !1), l.add(o));
  }
  function Tc(n, r, l) {
    var o = 0;
    r && (o |= 4), Nv(l, n, o, r);
  }
  var bc = "_reactListening" + Math.random().toString(36).slice(2);
  function mo(n) {
    if (!n[bc]) {
      n[bc] = !0, oe.forEach(function(l) {
        l !== "selectionchange" && (Sd.has(l) || Tc(l, !1, n), Tc(l, !0, n));
      });
      var r = n.nodeType === 9 ? n : n.ownerDocument;
      r === null || r[bc] || (r[bc] = !0, Tc("selectionchange", !1, r));
    }
  }
  function Nv(n, r, l, o) {
    switch (co(r)) {
      case 1:
        var c = uo;
        break;
      case 4:
        c = oo;
        break;
      default:
        c = kl;
    }
    l = c.bind(null, r, l, n), c = void 0, !Dr || r !== "touchstart" && r !== "touchmove" && r !== "wheel" || (c = !0), o ? c !== void 0 ? n.addEventListener(r, l, { capture: !0, passive: c }) : n.addEventListener(r, l, !0) : c !== void 0 ? n.addEventListener(r, l, { passive: c }) : n.addEventListener(r, l, !1);
  }
  function wc(n, r, l, o, c) {
    var d = o;
    if (!(r & 1) && !(r & 2) && o !== null) e: for (; ; ) {
      if (o === null) return;
      var m = o.tag;
      if (m === 3 || m === 4) {
        var E = o.stateNode.containerInfo;
        if (E === c || E.nodeType === 8 && E.parentNode === c) break;
        if (m === 4) for (m = o.return; m !== null; ) {
          var R = m.tag;
          if ((R === 3 || R === 4) && (R = m.stateNode.containerInfo, R === c || R.nodeType === 8 && R.parentNode === c)) return;
          m = m.return;
        }
        for (; E !== null; ) {
          if (m = Cu(E), m === null) return;
          if (R = m.tag, R === 5 || R === 6) {
            o = d = m;
            continue e;
          }
          E = E.parentNode;
        }
      }
      o = o.return;
    }
    ou(function() {
      var j = d, W = It(l), q = [];
      e: {
        var Q = yd.get(n);
        if (Q !== void 0) {
          var pe = vt, Se = n;
          switch (n) {
            case "keypress":
              if (H(l) === 0) break e;
            case "keydown":
            case "keyup":
              pe = ud;
              break;
            case "focusin":
              Se = "focus", pe = hu;
              break;
            case "focusout":
              Se = "blur", pe = hu;
              break;
            case "beforeblur":
            case "afterblur":
              pe = hu;
              break;
            case "click":
              if (l.button === 2) break e;
            case "auxclick":
            case "dblclick":
            case "mousedown":
            case "mousemove":
            case "mouseup":
            case "mouseout":
            case "mouseover":
            case "contextmenu":
              pe = Dl;
              break;
            case "drag":
            case "dragend":
            case "dragenter":
            case "dragexit":
            case "dragleave":
            case "dragover":
            case "dragstart":
            case "drop":
              pe = Qi;
              break;
            case "touchcancel":
            case "touchend":
            case "touchmove":
            case "touchstart":
              pe = dv;
              break;
            case xv:
            case kv:
            case Dv:
              pe = hc;
              break;
            case Ov:
              pe = Gi;
              break;
            case "scroll":
              pe = rn;
              break;
            case "wheel":
              pe = qi;
              break;
            case "copy":
            case "cut":
            case "paste":
              pe = ov;
              break;
            case "gotpointercapture":
            case "lostpointercapture":
            case "pointercancel":
            case "pointerdown":
            case "pointermove":
            case "pointerout":
            case "pointerover":
            case "pointerup":
              pe = fv;
          }
          var _e = (r & 4) !== 0, Dn = !_e && n === "scroll", D = _e ? Q !== null ? Q + "Capture" : null : Q;
          _e = [];
          for (var w = j, M; w !== null; ) {
            M = w;
            var G = M.stateNode;
            if (M.tag === 5 && G !== null && (M = G, D !== null && (G = kr(w, D), G != null && _e.push(yo(w, G, M)))), Dn) break;
            w = w.return;
          }
          0 < _e.length && (Q = new pe(Q, Se, null, l, W), q.push({ event: Q, listeners: _e }));
        }
      }
      if (!(r & 7)) {
        e: {
          if (Q = n === "mouseover" || n === "pointerover", pe = n === "mouseout" || n === "pointerout", Q && l !== tn && (Se = l.relatedTarget || l.fromElement) && (Cu(Se) || Se[Ki])) break e;
          if ((pe || Q) && (Q = W.window === W ? W : (Q = W.ownerDocument) ? Q.defaultView || Q.parentWindow : window, pe ? (Se = l.relatedTarget || l.toElement, pe = j, Se = Se ? Cu(Se) : null, Se !== null && (Dn = Ze(Se), Se !== Dn || Se.tag !== 5 && Se.tag !== 6) && (Se = null)) : (pe = null, Se = j), pe !== Se)) {
            if (_e = Dl, G = "onMouseLeave", D = "onMouseEnter", w = "mouse", (n === "pointerout" || n === "pointerover") && (_e = fv, G = "onPointerLeave", D = "onPointerEnter", w = "pointer"), Dn = pe == null ? Q : li(pe), M = Se == null ? Q : li(Se), Q = new _e(G, w + "leave", pe, l, W), Q.target = Dn, Q.relatedTarget = M, G = null, Cu(W) === j && (_e = new _e(D, w + "enter", Se, l, W), _e.target = M, _e.relatedTarget = Dn, G = _e), Dn = G, pe && Se) t: {
              for (_e = pe, D = Se, w = 0, M = _e; M; M = Nl(M)) w++;
              for (M = 0, G = D; G; G = Nl(G)) M++;
              for (; 0 < w - M; ) _e = Nl(_e), w--;
              for (; 0 < M - w; ) D = Nl(D), M--;
              for (; w--; ) {
                if (_e === D || D !== null && _e === D.alternate) break t;
                _e = Nl(_e), D = Nl(D);
              }
              _e = null;
            }
            else _e = null;
            pe !== null && Lv(q, Q, pe, _e, !1), Se !== null && Dn !== null && Lv(q, Dn, Se, _e, !0);
          }
        }
        e: {
          if (Q = j ? li(j) : window, pe = Q.nodeName && Q.nodeName.toLowerCase(), pe === "select" || pe === "input" && Q.type === "file") var Ee = uy;
          else if (gv(Q)) if (Ev) Ee = bv;
          else {
            Ee = Tv;
            var ze = oy;
          }
          else (pe = Q.nodeName) && pe.toLowerCase() === "input" && (Q.type === "checkbox" || Q.type === "radio") && (Ee = sy);
          if (Ee && (Ee = Ee(n, j))) {
            cd(q, Ee, l, W);
            break e;
          }
          ze && ze(n, Q, j), n === "focusout" && (ze = Q._wrapperState) && ze.controlled && Q.type === "number" && fa(Q, "number", Q.value);
        }
        switch (ze = j ? li(j) : window, n) {
          case "focusin":
            (gv(ze) || ze.contentEditable === "true") && (ho = ze, pd = j, ss = null);
            break;
          case "focusout":
            ss = pd = ho = null;
            break;
          case "mousedown":
            vd = !0;
            break;
          case "contextmenu":
          case "mouseup":
          case "dragend":
            vd = !1, hd(q, l, W);
            break;
          case "selectionchange":
            if (fy) break;
          case "keydown":
          case "keyup":
            hd(q, l, W);
        }
        var je;
        if (fo) e: {
          switch (n) {
            case "compositionstart":
              var Ye = "onCompositionStart";
              break e;
            case "compositionend":
              Ye = "onCompositionEnd";
              break e;
            case "compositionupdate":
              Ye = "onCompositionUpdate";
              break e;
          }
          Ye = void 0;
        }
        else po ? hv(n, l) && (Ye = "onCompositionEnd") : n === "keydown" && l.keyCode === 229 && (Ye = "onCompositionStart");
        Ye && (pv && l.locale !== "ko" && (po || Ye !== "onCompositionStart" ? Ye === "onCompositionEnd" && po && (je = z()) : (ai = W, h = "value" in ai ? ai.value : ai.textContent, po = !0)), ze = fs(j, Ye), 0 < ze.length && (Ye = new ad(Ye, n, null, l, W), q.push({ event: Ye, listeners: ze }), je ? Ye.data = je : (je = mv(l), je !== null && (Ye.data = je)))), (je = is ? yv(n, l) : iy(n, l)) && (j = fs(j, "onBeforeInput"), 0 < j.length && (W = new ad("onBeforeInput", "beforeinput", null, l, W), q.push({ event: W, listeners: j }), W.data = je));
      }
      Su(q, r);
    });
  }
  function yo(n, r, l) {
    return { instance: n, listener: r, currentTarget: l };
  }
  function fs(n, r) {
    for (var l = r + "Capture", o = []; n !== null; ) {
      var c = n, d = c.stateNode;
      c.tag === 5 && d !== null && (c = d, d = kr(n, l), d != null && o.unshift(yo(n, d, c)), d = kr(n, r), d != null && o.push(yo(n, d, c))), n = n.return;
    }
    return o;
  }
  function Nl(n) {
    if (n === null) return null;
    do
      n = n.return;
    while (n && n.tag !== 5);
    return n || null;
  }
  function Lv(n, r, l, o, c) {
    for (var d = r._reactName, m = []; l !== null && l !== o; ) {
      var E = l, R = E.alternate, j = E.stateNode;
      if (R !== null && R === o) break;
      E.tag === 5 && j !== null && (E = j, c ? (R = kr(l, d), R != null && m.unshift(yo(l, R, E))) : c || (R = kr(l, d), R != null && m.push(yo(l, R, E)))), l = l.return;
    }
    m.length !== 0 && n.push({ event: r, listeners: m });
  }
  var Mv = /\r\n?/g, vy = /\u0000|\uFFFD/g;
  function Uv(n) {
    return (typeof n == "string" ? n : "" + n).replace(Mv, `
`).replace(vy, "");
  }
  function xc(n, r, l) {
    if (r = Uv(r), Uv(n) !== r && l) throw Error(T(425));
  }
  function Ll() {
  }
  var ds = null, Eu = null;
  function kc(n, r) {
    return n === "textarea" || n === "noscript" || typeof r.children == "string" || typeof r.children == "number" || typeof r.dangerouslySetInnerHTML == "object" && r.dangerouslySetInnerHTML !== null && r.dangerouslySetInnerHTML.__html != null;
  }
  var Dc = typeof setTimeout == "function" ? setTimeout : void 0, Ed = typeof clearTimeout == "function" ? clearTimeout : void 0, zv = typeof Promise == "function" ? Promise : void 0, go = typeof queueMicrotask == "function" ? queueMicrotask : typeof zv < "u" ? function(n) {
    return zv.resolve(null).then(n).catch(Oc);
  } : Dc;
  function Oc(n) {
    setTimeout(function() {
      throw n;
    });
  }
  function So(n, r) {
    var l = r, o = 0;
    do {
      var c = l.nextSibling;
      if (n.removeChild(l), c && c.nodeType === 8) if (l = c.data, l === "/$") {
        if (o === 0) {
          n.removeChild(c), ri(r);
          return;
        }
        o--;
      } else l !== "$" && l !== "$?" && l !== "$!" || o++;
      l = c;
    } while (l);
    ri(r);
  }
  function Ti(n) {
    for (; n != null; n = n.nextSibling) {
      var r = n.nodeType;
      if (r === 1 || r === 3) break;
      if (r === 8) {
        if (r = n.data, r === "$" || r === "$!" || r === "$?") break;
        if (r === "/$") return null;
      }
    }
    return n;
  }
  function Av(n) {
    n = n.previousSibling;
    for (var r = 0; n; ) {
      if (n.nodeType === 8) {
        var l = n.data;
        if (l === "$" || l === "$!" || l === "$?") {
          if (r === 0) return n;
          r--;
        } else l === "/$" && r++;
      }
      n = n.previousSibling;
    }
    return null;
  }
  var Ml = Math.random().toString(36).slice(2), bi = "__reactFiber$" + Ml, ps = "__reactProps$" + Ml, Ki = "__reactContainer$" + Ml, vs = "__reactEvents$" + Ml, Eo = "__reactListeners$" + Ml, hy = "__reactHandles$" + Ml;
  function Cu(n) {
    var r = n[bi];
    if (r) return r;
    for (var l = n.parentNode; l; ) {
      if (r = l[Ki] || l[bi]) {
        if (l = r.alternate, r.child !== null || l !== null && l.child !== null) for (n = Av(n); n !== null; ) {
          if (l = n[bi]) return l;
          n = Av(n);
        }
        return r;
      }
      n = l, l = n.parentNode;
    }
    return null;
  }
  function Oe(n) {
    return n = n[bi] || n[Ki], !n || n.tag !== 5 && n.tag !== 6 && n.tag !== 13 && n.tag !== 3 ? null : n;
  }
  function li(n) {
    if (n.tag === 5 || n.tag === 6) return n.stateNode;
    throw Error(T(33));
  }
  function yn(n) {
    return n[ps] || null;
  }
  var Ct = [], La = -1;
  function Ma(n) {
    return { current: n };
  }
  function an(n) {
    0 > La || (n.current = Ct[La], Ct[La] = null, La--);
  }
  function xe(n, r) {
    La++, Ct[La] = n.current, n.current = r;
  }
  var Rr = {}, Cn = Ma(Rr), Wn = Ma(!1), Kr = Rr;
  function Xr(n, r) {
    var l = n.type.contextTypes;
    if (!l) return Rr;
    var o = n.stateNode;
    if (o && o.__reactInternalMemoizedUnmaskedChildContext === r) return o.__reactInternalMemoizedMaskedChildContext;
    var c = {}, d;
    for (d in l) c[d] = r[d];
    return o && (n = n.stateNode, n.__reactInternalMemoizedUnmaskedChildContext = r, n.__reactInternalMemoizedMaskedChildContext = c), c;
  }
  function Un(n) {
    return n = n.childContextTypes, n != null;
  }
  function Co() {
    an(Wn), an(Cn);
  }
  function jv(n, r, l) {
    if (Cn.current !== Rr) throw Error(T(168));
    xe(Cn, r), xe(Wn, l);
  }
  function hs(n, r, l) {
    var o = n.stateNode;
    if (r = r.childContextTypes, typeof o.getChildContext != "function") return l;
    o = o.getChildContext();
    for (var c in o) if (!(c in r)) throw Error(T(108, tt(n) || "Unknown", c));
    return ie({}, l, o);
  }
  function Jn(n) {
    return n = (n = n.stateNode) && n.__reactInternalMemoizedMergedChildContext || Rr, Kr = Cn.current, xe(Cn, n), xe(Wn, Wn.current), !0;
  }
  function Nc(n, r, l) {
    var o = n.stateNode;
    if (!o) throw Error(T(169));
    l ? (n = hs(n, r, Kr), o.__reactInternalMemoizedMergedChildContext = n, an(Wn), an(Cn), xe(Cn, n)) : an(Wn), xe(Wn, l);
  }
  var wi = null, _o = !1, Xi = !1;
  function Lc(n) {
    wi === null ? wi = [n] : wi.push(n);
  }
  function Ul(n) {
    _o = !0, Lc(n);
  }
  function xi() {
    if (!Xi && wi !== null) {
      Xi = !0;
      var n = 0, r = Lt;
      try {
        var l = wi;
        for (Lt = 1; n < l.length; n++) {
          var o = l[n];
          do
            o = o(!0);
          while (o !== null);
        }
        wi = null, _o = !1;
      } catch (c) {
        throw wi !== null && (wi = wi.slice(n + 1)), sn(ei, xi), c;
      } finally {
        Lt = r, Xi = !1;
      }
    }
    return null;
  }
  var zl = [], Al = 0, jl = null, Zi = 0, zn = [], Ua = 0, ha = null, ki = 1, Di = "";
  function _u(n, r) {
    zl[Al++] = Zi, zl[Al++] = jl, jl = n, Zi = r;
  }
  function Fv(n, r, l) {
    zn[Ua++] = ki, zn[Ua++] = Di, zn[Ua++] = ha, ha = n;
    var o = ki;
    n = Di;
    var c = 32 - Or(o) - 1;
    o &= ~(1 << c), l += 1;
    var d = 32 - Or(r) + c;
    if (30 < d) {
      var m = c - c % 5;
      d = (o & (1 << m) - 1).toString(32), o >>= m, c -= m, ki = 1 << 32 - Or(r) + c | l << c | o, Di = d + n;
    } else ki = 1 << d | l << c | o, Di = n;
  }
  function Mc(n) {
    n.return !== null && (_u(n, 1), Fv(n, 1, 0));
  }
  function Uc(n) {
    for (; n === jl; ) jl = zl[--Al], zl[Al] = null, Zi = zl[--Al], zl[Al] = null;
    for (; n === ha; ) ha = zn[--Ua], zn[Ua] = null, Di = zn[--Ua], zn[Ua] = null, ki = zn[--Ua], zn[Ua] = null;
  }
  var Zr = null, Jr = null, pn = !1, za = null;
  function Cd(n, r) {
    var l = Va(5, null, null, 0);
    l.elementType = "DELETED", l.stateNode = r, l.return = n, r = n.deletions, r === null ? (n.deletions = [l], n.flags |= 16) : r.push(l);
  }
  function Hv(n, r) {
    switch (n.tag) {
      case 5:
        var l = n.type;
        return r = r.nodeType !== 1 || l.toLowerCase() !== r.nodeName.toLowerCase() ? null : r, r !== null ? (n.stateNode = r, Zr = n, Jr = Ti(r.firstChild), !0) : !1;
      case 6:
        return r = n.pendingProps === "" || r.nodeType !== 3 ? null : r, r !== null ? (n.stateNode = r, Zr = n, Jr = null, !0) : !1;
      case 13:
        return r = r.nodeType !== 8 ? null : r, r !== null ? (l = ha !== null ? { id: ki, overflow: Di } : null, n.memoizedState = { dehydrated: r, treeContext: l, retryLane: 1073741824 }, l = Va(18, null, null, 0), l.stateNode = r, l.return = n, n.child = l, Zr = n, Jr = null, !0) : !1;
      default:
        return !1;
    }
  }
  function _d(n) {
    return (n.mode & 1) !== 0 && (n.flags & 128) === 0;
  }
  function Rd(n) {
    if (pn) {
      var r = Jr;
      if (r) {
        var l = r;
        if (!Hv(n, r)) {
          if (_d(n)) throw Error(T(418));
          r = Ti(l.nextSibling);
          var o = Zr;
          r && Hv(n, r) ? Cd(o, l) : (n.flags = n.flags & -4097 | 2, pn = !1, Zr = n);
        }
      } else {
        if (_d(n)) throw Error(T(418));
        n.flags = n.flags & -4097 | 2, pn = !1, Zr = n;
      }
    }
  }
  function Gn(n) {
    for (n = n.return; n !== null && n.tag !== 5 && n.tag !== 3 && n.tag !== 13; ) n = n.return;
    Zr = n;
  }
  function zc(n) {
    if (n !== Zr) return !1;
    if (!pn) return Gn(n), pn = !0, !1;
    var r;
    if ((r = n.tag !== 3) && !(r = n.tag !== 5) && (r = n.type, r = r !== "head" && r !== "body" && !kc(n.type, n.memoizedProps)), r && (r = Jr)) {
      if (_d(n)) throw ms(), Error(T(418));
      for (; r; ) Cd(n, r), r = Ti(r.nextSibling);
    }
    if (Gn(n), n.tag === 13) {
      if (n = n.memoizedState, n = n !== null ? n.dehydrated : null, !n) throw Error(T(317));
      e: {
        for (n = n.nextSibling, r = 0; n; ) {
          if (n.nodeType === 8) {
            var l = n.data;
            if (l === "/$") {
              if (r === 0) {
                Jr = Ti(n.nextSibling);
                break e;
              }
              r--;
            } else l !== "$" && l !== "$!" && l !== "$?" || r++;
          }
          n = n.nextSibling;
        }
        Jr = null;
      }
    } else Jr = Zr ? Ti(n.stateNode.nextSibling) : null;
    return !0;
  }
  function ms() {
    for (var n = Jr; n; ) n = Ti(n.nextSibling);
  }
  function Fl() {
    Jr = Zr = null, pn = !1;
  }
  function Ji(n) {
    za === null ? za = [n] : za.push(n);
  }
  var my = yt.ReactCurrentBatchConfig;
  function Ru(n, r, l) {
    if (n = l.ref, n !== null && typeof n != "function" && typeof n != "object") {
      if (l._owner) {
        if (l = l._owner, l) {
          if (l.tag !== 1) throw Error(T(309));
          var o = l.stateNode;
        }
        if (!o) throw Error(T(147, n));
        var c = o, d = "" + n;
        return r !== null && r.ref !== null && typeof r.ref == "function" && r.ref._stringRef === d ? r.ref : (r = function(m) {
          var E = c.refs;
          m === null ? delete E[d] : E[d] = m;
        }, r._stringRef = d, r);
      }
      if (typeof n != "string") throw Error(T(284));
      if (!l._owner) throw Error(T(290, n));
    }
    return n;
  }
  function Ac(n, r) {
    throw n = Object.prototype.toString.call(r), Error(T(31, n === "[object Object]" ? "object with keys {" + Object.keys(r).join(", ") + "}" : n));
  }
  function Vv(n) {
    var r = n._init;
    return r(n._payload);
  }
  function Tu(n) {
    function r(D, w) {
      if (n) {
        var M = D.deletions;
        M === null ? (D.deletions = [w], D.flags |= 16) : M.push(w);
      }
    }
    function l(D, w) {
      if (!n) return null;
      for (; w !== null; ) r(D, w), w = w.sibling;
      return null;
    }
    function o(D, w) {
      for (D = /* @__PURE__ */ new Map(); w !== null; ) w.key !== null ? D.set(w.key, w) : D.set(w.index, w), w = w.sibling;
      return D;
    }
    function c(D, w) {
      return D = Ql(D, w), D.index = 0, D.sibling = null, D;
    }
    function d(D, w, M) {
      return D.index = M, n ? (M = D.alternate, M !== null ? (M = M.index, M < w ? (D.flags |= 2, w) : M) : (D.flags |= 2, w)) : (D.flags |= 1048576, w);
    }
    function m(D) {
      return n && D.alternate === null && (D.flags |= 2), D;
    }
    function E(D, w, M, G) {
      return w === null || w.tag !== 6 ? (w = ep(M, D.mode, G), w.return = D, w) : (w = c(w, M), w.return = D, w);
    }
    function R(D, w, M, G) {
      var Ee = M.type;
      return Ee === Be ? W(D, w, M.props.children, G, M.key) : w !== null && (w.elementType === Ee || typeof Ee == "object" && Ee !== null && Ee.$$typeof === Nt && Vv(Ee) === w.type) ? (G = c(w, M.props), G.ref = Ru(D, w, M), G.return = D, G) : (G = Qs(M.type, M.key, M.props, null, D.mode, G), G.ref = Ru(D, w, M), G.return = D, G);
    }
    function j(D, w, M, G) {
      return w === null || w.tag !== 4 || w.stateNode.containerInfo !== M.containerInfo || w.stateNode.implementation !== M.implementation ? (w = mf(M, D.mode, G), w.return = D, w) : (w = c(w, M.children || []), w.return = D, w);
    }
    function W(D, w, M, G, Ee) {
      return w === null || w.tag !== 7 ? (w = il(M, D.mode, G, Ee), w.return = D, w) : (w = c(w, M), w.return = D, w);
    }
    function q(D, w, M) {
      if (typeof w == "string" && w !== "" || typeof w == "number") return w = ep("" + w, D.mode, M), w.return = D, w;
      if (typeof w == "object" && w !== null) {
        switch (w.$$typeof) {
          case De:
            return M = Qs(w.type, w.key, w.props, null, D.mode, M), M.ref = Ru(D, null, w), M.return = D, M;
          case dt:
            return w = mf(w, D.mode, M), w.return = D, w;
          case Nt:
            var G = w._init;
            return q(D, G(w._payload), M);
        }
        if (Xn(w) || Te(w)) return w = il(w, D.mode, M, null), w.return = D, w;
        Ac(D, w);
      }
      return null;
    }
    function Q(D, w, M, G) {
      var Ee = w !== null ? w.key : null;
      if (typeof M == "string" && M !== "" || typeof M == "number") return Ee !== null ? null : E(D, w, "" + M, G);
      if (typeof M == "object" && M !== null) {
        switch (M.$$typeof) {
          case De:
            return M.key === Ee ? R(D, w, M, G) : null;
          case dt:
            return M.key === Ee ? j(D, w, M, G) : null;
          case Nt:
            return Ee = M._init, Q(
              D,
              w,
              Ee(M._payload),
              G
            );
        }
        if (Xn(M) || Te(M)) return Ee !== null ? null : W(D, w, M, G, null);
        Ac(D, M);
      }
      return null;
    }
    function pe(D, w, M, G, Ee) {
      if (typeof G == "string" && G !== "" || typeof G == "number") return D = D.get(M) || null, E(w, D, "" + G, Ee);
      if (typeof G == "object" && G !== null) {
        switch (G.$$typeof) {
          case De:
            return D = D.get(G.key === null ? M : G.key) || null, R(w, D, G, Ee);
          case dt:
            return D = D.get(G.key === null ? M : G.key) || null, j(w, D, G, Ee);
          case Nt:
            var ze = G._init;
            return pe(D, w, M, ze(G._payload), Ee);
        }
        if (Xn(G) || Te(G)) return D = D.get(M) || null, W(w, D, G, Ee, null);
        Ac(w, G);
      }
      return null;
    }
    function Se(D, w, M, G) {
      for (var Ee = null, ze = null, je = w, Ye = w = 0, nr = null; je !== null && Ye < M.length; Ye++) {
        je.index > Ye ? (nr = je, je = null) : nr = je.sibling;
        var zt = Q(D, je, M[Ye], G);
        if (zt === null) {
          je === null && (je = nr);
          break;
        }
        n && je && zt.alternate === null && r(D, je), w = d(zt, w, Ye), ze === null ? Ee = zt : ze.sibling = zt, ze = zt, je = nr;
      }
      if (Ye === M.length) return l(D, je), pn && _u(D, Ye), Ee;
      if (je === null) {
        for (; Ye < M.length; Ye++) je = q(D, M[Ye], G), je !== null && (w = d(je, w, Ye), ze === null ? Ee = je : ze.sibling = je, ze = je);
        return pn && _u(D, Ye), Ee;
      }
      for (je = o(D, je); Ye < M.length; Ye++) nr = pe(je, D, Ye, M[Ye], G), nr !== null && (n && nr.alternate !== null && je.delete(nr.key === null ? Ye : nr.key), w = d(nr, w, Ye), ze === null ? Ee = nr : ze.sibling = nr, ze = nr);
      return n && je.forEach(function(ql) {
        return r(D, ql);
      }), pn && _u(D, Ye), Ee;
    }
    function _e(D, w, M, G) {
      var Ee = Te(M);
      if (typeof Ee != "function") throw Error(T(150));
      if (M = Ee.call(M), M == null) throw Error(T(151));
      for (var ze = Ee = null, je = w, Ye = w = 0, nr = null, zt = M.next(); je !== null && !zt.done; Ye++, zt = M.next()) {
        je.index > Ye ? (nr = je, je = null) : nr = je.sibling;
        var ql = Q(D, je, zt.value, G);
        if (ql === null) {
          je === null && (je = nr);
          break;
        }
        n && je && ql.alternate === null && r(D, je), w = d(ql, w, Ye), ze === null ? Ee = ql : ze.sibling = ql, ze = ql, je = nr;
      }
      if (zt.done) return l(
        D,
        je
      ), pn && _u(D, Ye), Ee;
      if (je === null) {
        for (; !zt.done; Ye++, zt = M.next()) zt = q(D, zt.value, G), zt !== null && (w = d(zt, w, Ye), ze === null ? Ee = zt : ze.sibling = zt, ze = zt);
        return pn && _u(D, Ye), Ee;
      }
      for (je = o(D, je); !zt.done; Ye++, zt = M.next()) zt = pe(je, D, Ye, zt.value, G), zt !== null && (n && zt.alternate !== null && je.delete(zt.key === null ? Ye : zt.key), w = d(zt, w, Ye), ze === null ? Ee = zt : ze.sibling = zt, ze = zt);
      return n && je.forEach(function(_h) {
        return r(D, _h);
      }), pn && _u(D, Ye), Ee;
    }
    function Dn(D, w, M, G) {
      if (typeof M == "object" && M !== null && M.type === Be && M.key === null && (M = M.props.children), typeof M == "object" && M !== null) {
        switch (M.$$typeof) {
          case De:
            e: {
              for (var Ee = M.key, ze = w; ze !== null; ) {
                if (ze.key === Ee) {
                  if (Ee = M.type, Ee === Be) {
                    if (ze.tag === 7) {
                      l(D, ze.sibling), w = c(ze, M.props.children), w.return = D, D = w;
                      break e;
                    }
                  } else if (ze.elementType === Ee || typeof Ee == "object" && Ee !== null && Ee.$$typeof === Nt && Vv(Ee) === ze.type) {
                    l(D, ze.sibling), w = c(ze, M.props), w.ref = Ru(D, ze, M), w.return = D, D = w;
                    break e;
                  }
                  l(D, ze);
                  break;
                } else r(D, ze);
                ze = ze.sibling;
              }
              M.type === Be ? (w = il(M.props.children, D.mode, G, M.key), w.return = D, D = w) : (G = Qs(M.type, M.key, M.props, null, D.mode, G), G.ref = Ru(D, w, M), G.return = D, D = G);
            }
            return m(D);
          case dt:
            e: {
              for (ze = M.key; w !== null; ) {
                if (w.key === ze) if (w.tag === 4 && w.stateNode.containerInfo === M.containerInfo && w.stateNode.implementation === M.implementation) {
                  l(D, w.sibling), w = c(w, M.children || []), w.return = D, D = w;
                  break e;
                } else {
                  l(D, w);
                  break;
                }
                else r(D, w);
                w = w.sibling;
              }
              w = mf(M, D.mode, G), w.return = D, D = w;
            }
            return m(D);
          case Nt:
            return ze = M._init, Dn(D, w, ze(M._payload), G);
        }
        if (Xn(M)) return Se(D, w, M, G);
        if (Te(M)) return _e(D, w, M, G);
        Ac(D, M);
      }
      return typeof M == "string" && M !== "" || typeof M == "number" ? (M = "" + M, w !== null && w.tag === 6 ? (l(D, w.sibling), w = c(w, M), w.return = D, D = w) : (l(D, w), w = ep(M, D.mode, G), w.return = D, D = w), m(D)) : l(D, w);
    }
    return Dn;
  }
  var bn = Tu(!0), se = Tu(!1), ma = Ma(null), ea = null, Ro = null, Td = null;
  function bd() {
    Td = Ro = ea = null;
  }
  function wd(n) {
    var r = ma.current;
    an(ma), n._currentValue = r;
  }
  function xd(n, r, l) {
    for (; n !== null; ) {
      var o = n.alternate;
      if ((n.childLanes & r) !== r ? (n.childLanes |= r, o !== null && (o.childLanes |= r)) : o !== null && (o.childLanes & r) !== r && (o.childLanes |= r), n === l) break;
      n = n.return;
    }
  }
  function gn(n, r) {
    ea = n, Td = Ro = null, n = n.dependencies, n !== null && n.firstContext !== null && (n.lanes & r && (jn = !0), n.firstContext = null);
  }
  function Aa(n) {
    var r = n._currentValue;
    if (Td !== n) if (n = { context: n, memoizedValue: r, next: null }, Ro === null) {
      if (ea === null) throw Error(T(308));
      Ro = n, ea.dependencies = { lanes: 0, firstContext: n };
    } else Ro = Ro.next = n;
    return r;
  }
  var bu = null;
  function kd(n) {
    bu === null ? bu = [n] : bu.push(n);
  }
  function Dd(n, r, l, o) {
    var c = r.interleaved;
    return c === null ? (l.next = l, kd(r)) : (l.next = c.next, c.next = l), r.interleaved = l, ya(n, o);
  }
  function ya(n, r) {
    n.lanes |= r;
    var l = n.alternate;
    for (l !== null && (l.lanes |= r), l = n, n = n.return; n !== null; ) n.childLanes |= r, l = n.alternate, l !== null && (l.childLanes |= r), l = n, n = n.return;
    return l.tag === 3 ? l.stateNode : null;
  }
  var ga = !1;
  function Od(n) {
    n.updateQueue = { baseState: n.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
  }
  function Pv(n, r) {
    n = n.updateQueue, r.updateQueue === n && (r.updateQueue = { baseState: n.baseState, firstBaseUpdate: n.firstBaseUpdate, lastBaseUpdate: n.lastBaseUpdate, shared: n.shared, effects: n.effects });
  }
  function el(n, r) {
    return { eventTime: n, lane: r, tag: 0, payload: null, callback: null, next: null };
  }
  function Hl(n, r, l) {
    var o = n.updateQueue;
    if (o === null) return null;
    if (o = o.shared, _t & 2) {
      var c = o.pending;
      return c === null ? r.next = r : (r.next = c.next, c.next = r), o.pending = r, ya(n, l);
    }
    return c = o.interleaved, c === null ? (r.next = r, kd(o)) : (r.next = c.next, c.next = r), o.interleaved = r, ya(n, l);
  }
  function jc(n, r, l) {
    if (r = r.updateQueue, r !== null && (r = r.shared, (l & 4194240) !== 0)) {
      var o = r.lanes;
      o &= n.pendingLanes, l |= o, r.lanes = l, Yi(n, l);
    }
  }
  function Bv(n, r) {
    var l = n.updateQueue, o = n.alternate;
    if (o !== null && (o = o.updateQueue, l === o)) {
      var c = null, d = null;
      if (l = l.firstBaseUpdate, l !== null) {
        do {
          var m = { eventTime: l.eventTime, lane: l.lane, tag: l.tag, payload: l.payload, callback: l.callback, next: null };
          d === null ? c = d = m : d = d.next = m, l = l.next;
        } while (l !== null);
        d === null ? c = d = r : d = d.next = r;
      } else c = d = r;
      l = { baseState: o.baseState, firstBaseUpdate: c, lastBaseUpdate: d, shared: o.shared, effects: o.effects }, n.updateQueue = l;
      return;
    }
    n = l.lastBaseUpdate, n === null ? l.firstBaseUpdate = r : n.next = r, l.lastBaseUpdate = r;
  }
  function ys(n, r, l, o) {
    var c = n.updateQueue;
    ga = !1;
    var d = c.firstBaseUpdate, m = c.lastBaseUpdate, E = c.shared.pending;
    if (E !== null) {
      c.shared.pending = null;
      var R = E, j = R.next;
      R.next = null, m === null ? d = j : m.next = j, m = R;
      var W = n.alternate;
      W !== null && (W = W.updateQueue, E = W.lastBaseUpdate, E !== m && (E === null ? W.firstBaseUpdate = j : E.next = j, W.lastBaseUpdate = R));
    }
    if (d !== null) {
      var q = c.baseState;
      m = 0, W = j = R = null, E = d;
      do {
        var Q = E.lane, pe = E.eventTime;
        if ((o & Q) === Q) {
          W !== null && (W = W.next = {
            eventTime: pe,
            lane: 0,
            tag: E.tag,
            payload: E.payload,
            callback: E.callback,
            next: null
          });
          e: {
            var Se = n, _e = E;
            switch (Q = r, pe = l, _e.tag) {
              case 1:
                if (Se = _e.payload, typeof Se == "function") {
                  q = Se.call(pe, q, Q);
                  break e;
                }
                q = Se;
                break e;
              case 3:
                Se.flags = Se.flags & -65537 | 128;
              case 0:
                if (Se = _e.payload, Q = typeof Se == "function" ? Se.call(pe, q, Q) : Se, Q == null) break e;
                q = ie({}, q, Q);
                break e;
              case 2:
                ga = !0;
            }
          }
          E.callback !== null && E.lane !== 0 && (n.flags |= 64, Q = c.effects, Q === null ? c.effects = [E] : Q.push(E));
        } else pe = { eventTime: pe, lane: Q, tag: E.tag, payload: E.payload, callback: E.callback, next: null }, W === null ? (j = W = pe, R = q) : W = W.next = pe, m |= Q;
        if (E = E.next, E === null) {
          if (E = c.shared.pending, E === null) break;
          Q = E, E = Q.next, Q.next = null, c.lastBaseUpdate = Q, c.shared.pending = null;
        }
      } while (!0);
      if (W === null && (R = q), c.baseState = R, c.firstBaseUpdate = j, c.lastBaseUpdate = W, r = c.shared.interleaved, r !== null) {
        c = r;
        do
          m |= c.lane, c = c.next;
        while (c !== r);
      } else d === null && (c.shared.lanes = 0);
      Ui |= m, n.lanes = m, n.memoizedState = q;
    }
  }
  function Nd(n, r, l) {
    if (n = r.effects, r.effects = null, n !== null) for (r = 0; r < n.length; r++) {
      var o = n[r], c = o.callback;
      if (c !== null) {
        if (o.callback = null, o = l, typeof c != "function") throw Error(T(191, c));
        c.call(o);
      }
    }
  }
  var gs = {}, Oi = Ma(gs), Ss = Ma(gs), Es = Ma(gs);
  function wu(n) {
    if (n === gs) throw Error(T(174));
    return n;
  }
  function Ld(n, r) {
    switch (xe(Es, r), xe(Ss, n), xe(Oi, gs), n = r.nodeType, n) {
      case 9:
      case 11:
        r = (r = r.documentElement) ? r.namespaceURI : da(null, "");
        break;
      default:
        n = n === 8 ? r.parentNode : r, r = n.namespaceURI || null, n = n.tagName, r = da(r, n);
    }
    an(Oi), xe(Oi, r);
  }
  function xu() {
    an(Oi), an(Ss), an(Es);
  }
  function $v(n) {
    wu(Es.current);
    var r = wu(Oi.current), l = da(r, n.type);
    r !== l && (xe(Ss, n), xe(Oi, l));
  }
  function Fc(n) {
    Ss.current === n && (an(Oi), an(Ss));
  }
  var Sn = Ma(0);
  function Hc(n) {
    for (var r = n; r !== null; ) {
      if (r.tag === 13) {
        var l = r.memoizedState;
        if (l !== null && (l = l.dehydrated, l === null || l.data === "$?" || l.data === "$!")) return r;
      } else if (r.tag === 19 && r.memoizedProps.revealOrder !== void 0) {
        if (r.flags & 128) return r;
      } else if (r.child !== null) {
        r.child.return = r, r = r.child;
        continue;
      }
      if (r === n) break;
      for (; r.sibling === null; ) {
        if (r.return === null || r.return === n) return null;
        r = r.return;
      }
      r.sibling.return = r.return, r = r.sibling;
    }
    return null;
  }
  var Cs = [];
  function Ne() {
    for (var n = 0; n < Cs.length; n++) Cs[n]._workInProgressVersionPrimary = null;
    Cs.length = 0;
  }
  var ct = yt.ReactCurrentDispatcher, Mt = yt.ReactCurrentBatchConfig, qt = 0, Ut = null, An = null, er = null, Vc = !1, _s = !1, ku = 0, Y = 0;
  function Ot() {
    throw Error(T(321));
  }
  function Pe(n, r) {
    if (r === null) return !1;
    for (var l = 0; l < r.length && l < n.length; l++) if (!ii(n[l], r[l])) return !1;
    return !0;
  }
  function Vl(n, r, l, o, c, d) {
    if (qt = d, Ut = r, r.memoizedState = null, r.updateQueue = null, r.lanes = 0, ct.current = n === null || n.memoizedState === null ? tf : ks, n = l(o, c), _s) {
      d = 0;
      do {
        if (_s = !1, ku = 0, 25 <= d) throw Error(T(301));
        d += 1, er = An = null, r.updateQueue = null, ct.current = nf, n = l(o, c);
      } while (_s);
    }
    if (ct.current = Mu, r = An !== null && An.next !== null, qt = 0, er = An = Ut = null, Vc = !1, r) throw Error(T(300));
    return n;
  }
  function ui() {
    var n = ku !== 0;
    return ku = 0, n;
  }
  function Tr() {
    var n = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
    return er === null ? Ut.memoizedState = er = n : er = er.next = n, er;
  }
  function wn() {
    if (An === null) {
      var n = Ut.alternate;
      n = n !== null ? n.memoizedState : null;
    } else n = An.next;
    var r = er === null ? Ut.memoizedState : er.next;
    if (r !== null) er = r, An = n;
    else {
      if (n === null) throw Error(T(310));
      An = n, n = { memoizedState: An.memoizedState, baseState: An.baseState, baseQueue: An.baseQueue, queue: An.queue, next: null }, er === null ? Ut.memoizedState = er = n : er = er.next = n;
    }
    return er;
  }
  function tl(n, r) {
    return typeof r == "function" ? r(n) : r;
  }
  function Pl(n) {
    var r = wn(), l = r.queue;
    if (l === null) throw Error(T(311));
    l.lastRenderedReducer = n;
    var o = An, c = o.baseQueue, d = l.pending;
    if (d !== null) {
      if (c !== null) {
        var m = c.next;
        c.next = d.next, d.next = m;
      }
      o.baseQueue = c = d, l.pending = null;
    }
    if (c !== null) {
      d = c.next, o = o.baseState;
      var E = m = null, R = null, j = d;
      do {
        var W = j.lane;
        if ((qt & W) === W) R !== null && (R = R.next = { lane: 0, action: j.action, hasEagerState: j.hasEagerState, eagerState: j.eagerState, next: null }), o = j.hasEagerState ? j.eagerState : n(o, j.action);
        else {
          var q = {
            lane: W,
            action: j.action,
            hasEagerState: j.hasEagerState,
            eagerState: j.eagerState,
            next: null
          };
          R === null ? (E = R = q, m = o) : R = R.next = q, Ut.lanes |= W, Ui |= W;
        }
        j = j.next;
      } while (j !== null && j !== d);
      R === null ? m = o : R.next = E, ii(o, r.memoizedState) || (jn = !0), r.memoizedState = o, r.baseState = m, r.baseQueue = R, l.lastRenderedState = o;
    }
    if (n = l.interleaved, n !== null) {
      c = n;
      do
        d = c.lane, Ut.lanes |= d, Ui |= d, c = c.next;
      while (c !== n);
    } else c === null && (l.lanes = 0);
    return [r.memoizedState, l.dispatch];
  }
  function Du(n) {
    var r = wn(), l = r.queue;
    if (l === null) throw Error(T(311));
    l.lastRenderedReducer = n;
    var o = l.dispatch, c = l.pending, d = r.memoizedState;
    if (c !== null) {
      l.pending = null;
      var m = c = c.next;
      do
        d = n(d, m.action), m = m.next;
      while (m !== c);
      ii(d, r.memoizedState) || (jn = !0), r.memoizedState = d, r.baseQueue === null && (r.baseState = d), l.lastRenderedState = d;
    }
    return [d, o];
  }
  function Pc() {
  }
  function Bc(n, r) {
    var l = Ut, o = wn(), c = r(), d = !ii(o.memoizedState, c);
    if (d && (o.memoizedState = c, jn = !0), o = o.queue, Rs(Yc.bind(null, l, o, n), [n]), o.getSnapshot !== r || d || er !== null && er.memoizedState.tag & 1) {
      if (l.flags |= 2048, Ou(9, Ic.bind(null, l, o, c, r), void 0, null), qn === null) throw Error(T(349));
      qt & 30 || $c(l, r, c);
    }
    return c;
  }
  function $c(n, r, l) {
    n.flags |= 16384, n = { getSnapshot: r, value: l }, r = Ut.updateQueue, r === null ? (r = { lastEffect: null, stores: null }, Ut.updateQueue = r, r.stores = [n]) : (l = r.stores, l === null ? r.stores = [n] : l.push(n));
  }
  function Ic(n, r, l, o) {
    r.value = l, r.getSnapshot = o, Qc(r) && Wc(n);
  }
  function Yc(n, r, l) {
    return l(function() {
      Qc(r) && Wc(n);
    });
  }
  function Qc(n) {
    var r = n.getSnapshot;
    n = n.value;
    try {
      var l = r();
      return !ii(n, l);
    } catch {
      return !0;
    }
  }
  function Wc(n) {
    var r = ya(n, 1);
    r !== null && Ar(r, n, 1, -1);
  }
  function Gc(n) {
    var r = Tr();
    return typeof n == "function" && (n = n()), r.memoizedState = r.baseState = n, n = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: tl, lastRenderedState: n }, r.queue = n, n = n.dispatch = Lu.bind(null, Ut, n), [r.memoizedState, n];
  }
  function Ou(n, r, l, o) {
    return n = { tag: n, create: r, destroy: l, deps: o, next: null }, r = Ut.updateQueue, r === null ? (r = { lastEffect: null, stores: null }, Ut.updateQueue = r, r.lastEffect = n.next = n) : (l = r.lastEffect, l === null ? r.lastEffect = n.next = n : (o = l.next, l.next = n, n.next = o, r.lastEffect = n)), n;
  }
  function qc() {
    return wn().memoizedState;
  }
  function To(n, r, l, o) {
    var c = Tr();
    Ut.flags |= n, c.memoizedState = Ou(1 | r, l, void 0, o === void 0 ? null : o);
  }
  function bo(n, r, l, o) {
    var c = wn();
    o = o === void 0 ? null : o;
    var d = void 0;
    if (An !== null) {
      var m = An.memoizedState;
      if (d = m.destroy, o !== null && Pe(o, m.deps)) {
        c.memoizedState = Ou(r, l, d, o);
        return;
      }
    }
    Ut.flags |= n, c.memoizedState = Ou(1 | r, l, d, o);
  }
  function Kc(n, r) {
    return To(8390656, 8, n, r);
  }
  function Rs(n, r) {
    return bo(2048, 8, n, r);
  }
  function Xc(n, r) {
    return bo(4, 2, n, r);
  }
  function Ts(n, r) {
    return bo(4, 4, n, r);
  }
  function Nu(n, r) {
    if (typeof r == "function") return n = n(), r(n), function() {
      r(null);
    };
    if (r != null) return n = n(), r.current = n, function() {
      r.current = null;
    };
  }
  function Zc(n, r, l) {
    return l = l != null ? l.concat([n]) : null, bo(4, 4, Nu.bind(null, r, n), l);
  }
  function bs() {
  }
  function Jc(n, r) {
    var l = wn();
    r = r === void 0 ? null : r;
    var o = l.memoizedState;
    return o !== null && r !== null && Pe(r, o[1]) ? o[0] : (l.memoizedState = [n, r], n);
  }
  function ef(n, r) {
    var l = wn();
    r = r === void 0 ? null : r;
    var o = l.memoizedState;
    return o !== null && r !== null && Pe(r, o[1]) ? o[0] : (n = n(), l.memoizedState = [n, r], n);
  }
  function Md(n, r, l) {
    return qt & 21 ? (ii(l, r) || (l = ro(), Ut.lanes |= l, Ui |= l, n.baseState = !0), r) : (n.baseState && (n.baseState = !1, jn = !0), n.memoizedState = l);
  }
  function ws(n, r) {
    var l = Lt;
    Lt = l !== 0 && 4 > l ? l : 4, n(!0);
    var o = Mt.transition;
    Mt.transition = {};
    try {
      n(!1), r();
    } finally {
      Lt = l, Mt.transition = o;
    }
  }
  function Ud() {
    return wn().memoizedState;
  }
  function xs(n, r, l) {
    var o = zi(n);
    if (l = { lane: o, action: l, hasEagerState: !1, eagerState: null, next: null }, ta(n)) Iv(r, l);
    else if (l = Dd(n, r, l, o), l !== null) {
      var c = Vn();
      Ar(l, n, o, c), Zt(l, r, o);
    }
  }
  function Lu(n, r, l) {
    var o = zi(n), c = { lane: o, action: l, hasEagerState: !1, eagerState: null, next: null };
    if (ta(n)) Iv(r, c);
    else {
      var d = n.alternate;
      if (n.lanes === 0 && (d === null || d.lanes === 0) && (d = r.lastRenderedReducer, d !== null)) try {
        var m = r.lastRenderedState, E = d(m, l);
        if (c.hasEagerState = !0, c.eagerState = E, ii(E, m)) {
          var R = r.interleaved;
          R === null ? (c.next = c, kd(r)) : (c.next = R.next, R.next = c), r.interleaved = c;
          return;
        }
      } catch {
      } finally {
      }
      l = Dd(n, r, c, o), l !== null && (c = Vn(), Ar(l, n, o, c), Zt(l, r, o));
    }
  }
  function ta(n) {
    var r = n.alternate;
    return n === Ut || r !== null && r === Ut;
  }
  function Iv(n, r) {
    _s = Vc = !0;
    var l = n.pending;
    l === null ? r.next = r : (r.next = l.next, l.next = r), n.pending = r;
  }
  function Zt(n, r, l) {
    if (l & 4194240) {
      var o = r.lanes;
      o &= n.pendingLanes, l |= o, r.lanes = l, Yi(n, l);
    }
  }
  var Mu = { readContext: Aa, useCallback: Ot, useContext: Ot, useEffect: Ot, useImperativeHandle: Ot, useInsertionEffect: Ot, useLayoutEffect: Ot, useMemo: Ot, useReducer: Ot, useRef: Ot, useState: Ot, useDebugValue: Ot, useDeferredValue: Ot, useTransition: Ot, useMutableSource: Ot, useSyncExternalStore: Ot, useId: Ot, unstable_isNewReconciler: !1 }, tf = { readContext: Aa, useCallback: function(n, r) {
    return Tr().memoizedState = [n, r === void 0 ? null : r], n;
  }, useContext: Aa, useEffect: Kc, useImperativeHandle: function(n, r, l) {
    return l = l != null ? l.concat([n]) : null, To(
      4194308,
      4,
      Nu.bind(null, r, n),
      l
    );
  }, useLayoutEffect: function(n, r) {
    return To(4194308, 4, n, r);
  }, useInsertionEffect: function(n, r) {
    return To(4, 2, n, r);
  }, useMemo: function(n, r) {
    var l = Tr();
    return r = r === void 0 ? null : r, n = n(), l.memoizedState = [n, r], n;
  }, useReducer: function(n, r, l) {
    var o = Tr();
    return r = l !== void 0 ? l(r) : r, o.memoizedState = o.baseState = r, n = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: n, lastRenderedState: r }, o.queue = n, n = n.dispatch = xs.bind(null, Ut, n), [o.memoizedState, n];
  }, useRef: function(n) {
    var r = Tr();
    return n = { current: n }, r.memoizedState = n;
  }, useState: Gc, useDebugValue: bs, useDeferredValue: function(n) {
    return Tr().memoizedState = n;
  }, useTransition: function() {
    var n = Gc(!1), r = n[0];
    return n = ws.bind(null, n[1]), Tr().memoizedState = n, [r, n];
  }, useMutableSource: function() {
  }, useSyncExternalStore: function(n, r, l) {
    var o = Ut, c = Tr();
    if (pn) {
      if (l === void 0) throw Error(T(407));
      l = l();
    } else {
      if (l = r(), qn === null) throw Error(T(349));
      qt & 30 || $c(o, r, l);
    }
    c.memoizedState = l;
    var d = { value: l, getSnapshot: r };
    return c.queue = d, Kc(Yc.bind(
      null,
      o,
      d,
      n
    ), [n]), o.flags |= 2048, Ou(9, Ic.bind(null, o, d, l, r), void 0, null), l;
  }, useId: function() {
    var n = Tr(), r = qn.identifierPrefix;
    if (pn) {
      var l = Di, o = ki;
      l = (o & ~(1 << 32 - Or(o) - 1)).toString(32) + l, r = ":" + r + "R" + l, l = ku++, 0 < l && (r += "H" + l.toString(32)), r += ":";
    } else l = Y++, r = ":" + r + "r" + l.toString(32) + ":";
    return n.memoizedState = r;
  }, unstable_isNewReconciler: !1 }, ks = {
    readContext: Aa,
    useCallback: Jc,
    useContext: Aa,
    useEffect: Rs,
    useImperativeHandle: Zc,
    useInsertionEffect: Xc,
    useLayoutEffect: Ts,
    useMemo: ef,
    useReducer: Pl,
    useRef: qc,
    useState: function() {
      return Pl(tl);
    },
    useDebugValue: bs,
    useDeferredValue: function(n) {
      var r = wn();
      return Md(r, An.memoizedState, n);
    },
    useTransition: function() {
      var n = Pl(tl)[0], r = wn().memoizedState;
      return [n, r];
    },
    useMutableSource: Pc,
    useSyncExternalStore: Bc,
    useId: Ud,
    unstable_isNewReconciler: !1
  }, nf = { readContext: Aa, useCallback: Jc, useContext: Aa, useEffect: Rs, useImperativeHandle: Zc, useInsertionEffect: Xc, useLayoutEffect: Ts, useMemo: ef, useReducer: Du, useRef: qc, useState: function() {
    return Du(tl);
  }, useDebugValue: bs, useDeferredValue: function(n) {
    var r = wn();
    return An === null ? r.memoizedState = n : Md(r, An.memoizedState, n);
  }, useTransition: function() {
    var n = Du(tl)[0], r = wn().memoizedState;
    return [n, r];
  }, useMutableSource: Pc, useSyncExternalStore: Bc, useId: Ud, unstable_isNewReconciler: !1 };
  function oi(n, r) {
    if (n && n.defaultProps) {
      r = ie({}, r), n = n.defaultProps;
      for (var l in n) r[l] === void 0 && (r[l] = n[l]);
      return r;
    }
    return r;
  }
  function zd(n, r, l, o) {
    r = n.memoizedState, l = l(o, r), l = l == null ? r : ie({}, r, l), n.memoizedState = l, n.lanes === 0 && (n.updateQueue.baseState = l);
  }
  var rf = { isMounted: function(n) {
    return (n = n._reactInternals) ? Ze(n) === n : !1;
  }, enqueueSetState: function(n, r, l) {
    n = n._reactInternals;
    var o = Vn(), c = zi(n), d = el(o, c);
    d.payload = r, l != null && (d.callback = l), r = Hl(n, d, c), r !== null && (Ar(r, n, c, o), jc(r, n, c));
  }, enqueueReplaceState: function(n, r, l) {
    n = n._reactInternals;
    var o = Vn(), c = zi(n), d = el(o, c);
    d.tag = 1, d.payload = r, l != null && (d.callback = l), r = Hl(n, d, c), r !== null && (Ar(r, n, c, o), jc(r, n, c));
  }, enqueueForceUpdate: function(n, r) {
    n = n._reactInternals;
    var l = Vn(), o = zi(n), c = el(l, o);
    c.tag = 2, r != null && (c.callback = r), r = Hl(n, c, o), r !== null && (Ar(r, n, o, l), jc(r, n, o));
  } };
  function Yv(n, r, l, o, c, d, m) {
    return n = n.stateNode, typeof n.shouldComponentUpdate == "function" ? n.shouldComponentUpdate(o, d, m) : r.prototype && r.prototype.isPureReactComponent ? !us(l, o) || !us(c, d) : !0;
  }
  function af(n, r, l) {
    var o = !1, c = Rr, d = r.contextType;
    return typeof d == "object" && d !== null ? d = Aa(d) : (c = Un(r) ? Kr : Cn.current, o = r.contextTypes, d = (o = o != null) ? Xr(n, c) : Rr), r = new r(l, d), n.memoizedState = r.state !== null && r.state !== void 0 ? r.state : null, r.updater = rf, n.stateNode = r, r._reactInternals = n, o && (n = n.stateNode, n.__reactInternalMemoizedUnmaskedChildContext = c, n.__reactInternalMemoizedMaskedChildContext = d), r;
  }
  function Qv(n, r, l, o) {
    n = r.state, typeof r.componentWillReceiveProps == "function" && r.componentWillReceiveProps(l, o), typeof r.UNSAFE_componentWillReceiveProps == "function" && r.UNSAFE_componentWillReceiveProps(l, o), r.state !== n && rf.enqueueReplaceState(r, r.state, null);
  }
  function Ds(n, r, l, o) {
    var c = n.stateNode;
    c.props = l, c.state = n.memoizedState, c.refs = {}, Od(n);
    var d = r.contextType;
    typeof d == "object" && d !== null ? c.context = Aa(d) : (d = Un(r) ? Kr : Cn.current, c.context = Xr(n, d)), c.state = n.memoizedState, d = r.getDerivedStateFromProps, typeof d == "function" && (zd(n, r, d, l), c.state = n.memoizedState), typeof r.getDerivedStateFromProps == "function" || typeof c.getSnapshotBeforeUpdate == "function" || typeof c.UNSAFE_componentWillMount != "function" && typeof c.componentWillMount != "function" || (r = c.state, typeof c.componentWillMount == "function" && c.componentWillMount(), typeof c.UNSAFE_componentWillMount == "function" && c.UNSAFE_componentWillMount(), r !== c.state && rf.enqueueReplaceState(c, c.state, null), ys(n, l, c, o), c.state = n.memoizedState), typeof c.componentDidMount == "function" && (n.flags |= 4194308);
  }
  function Uu(n, r) {
    try {
      var l = "", o = r;
      do
        l += ut(o), o = o.return;
      while (o);
      var c = l;
    } catch (d) {
      c = `
Error generating stack: ` + d.message + `
` + d.stack;
    }
    return { value: n, source: r, stack: c, digest: null };
  }
  function Ad(n, r, l) {
    return { value: n, source: null, stack: l ?? null, digest: r ?? null };
  }
  function jd(n, r) {
    try {
      console.error(r.value);
    } catch (l) {
      setTimeout(function() {
        throw l;
      });
    }
  }
  var lf = typeof WeakMap == "function" ? WeakMap : Map;
  function Wv(n, r, l) {
    l = el(-1, l), l.tag = 3, l.payload = { element: null };
    var o = r.value;
    return l.callback = function() {
      No || (No = !0, ju = o), jd(n, r);
    }, l;
  }
  function Fd(n, r, l) {
    l = el(-1, l), l.tag = 3;
    var o = n.type.getDerivedStateFromError;
    if (typeof o == "function") {
      var c = r.value;
      l.payload = function() {
        return o(c);
      }, l.callback = function() {
        jd(n, r);
      };
    }
    var d = n.stateNode;
    return d !== null && typeof d.componentDidCatch == "function" && (l.callback = function() {
      jd(n, r), typeof o != "function" && (Il === null ? Il = /* @__PURE__ */ new Set([this]) : Il.add(this));
      var m = r.stack;
      this.componentDidCatch(r.value, { componentStack: m !== null ? m : "" });
    }), l;
  }
  function Hd(n, r, l) {
    var o = n.pingCache;
    if (o === null) {
      o = n.pingCache = new lf();
      var c = /* @__PURE__ */ new Set();
      o.set(r, c);
    } else c = o.get(r), c === void 0 && (c = /* @__PURE__ */ new Set(), o.set(r, c));
    c.has(l) || (c.add(l), n = Ry.bind(null, n, r, l), r.then(n, n));
  }
  function Gv(n) {
    do {
      var r;
      if ((r = n.tag === 13) && (r = n.memoizedState, r = r !== null ? r.dehydrated !== null : !0), r) return n;
      n = n.return;
    } while (n !== null);
    return null;
  }
  function Bl(n, r, l, o, c) {
    return n.mode & 1 ? (n.flags |= 65536, n.lanes = c, n) : (n === r ? n.flags |= 65536 : (n.flags |= 128, l.flags |= 131072, l.flags &= -52805, l.tag === 1 && (l.alternate === null ? l.tag = 17 : (r = el(-1, 1), r.tag = 2, Hl(l, r, 1))), l.lanes |= 1), n);
  }
  var Os = yt.ReactCurrentOwner, jn = !1;
  function sr(n, r, l, o) {
    r.child = n === null ? se(r, null, l, o) : bn(r, n.child, l, o);
  }
  function na(n, r, l, o, c) {
    l = l.render;
    var d = r.ref;
    return gn(r, c), o = Vl(n, r, l, o, d, c), l = ui(), n !== null && !jn ? (r.updateQueue = n.updateQueue, r.flags &= -2053, n.lanes &= ~c, Fa(n, r, c)) : (pn && l && Mc(r), r.flags |= 1, sr(n, r, o, c), r.child);
  }
  function zu(n, r, l, o, c) {
    if (n === null) {
      var d = l.type;
      return typeof d == "function" && !Jd(d) && d.defaultProps === void 0 && l.compare === null && l.defaultProps === void 0 ? (r.tag = 15, r.type = d, et(n, r, d, o, c)) : (n = Qs(l.type, null, o, r, r.mode, c), n.ref = r.ref, n.return = r, r.child = n);
    }
    if (d = n.child, !(n.lanes & c)) {
      var m = d.memoizedProps;
      if (l = l.compare, l = l !== null ? l : us, l(m, o) && n.ref === r.ref) return Fa(n, r, c);
    }
    return r.flags |= 1, n = Ql(d, o), n.ref = r.ref, n.return = r, r.child = n;
  }
  function et(n, r, l, o, c) {
    if (n !== null) {
      var d = n.memoizedProps;
      if (us(d, o) && n.ref === r.ref) if (jn = !1, r.pendingProps = o = d, (n.lanes & c) !== 0) n.flags & 131072 && (jn = !0);
      else return r.lanes = n.lanes, Fa(n, r, c);
    }
    return qv(n, r, l, o, c);
  }
  function Ns(n, r, l) {
    var o = r.pendingProps, c = o.children, d = n !== null ? n.memoizedState : null;
    if (o.mode === "hidden") if (!(r.mode & 1)) r.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, xe(ko, Sa), Sa |= l;
    else {
      if (!(l & 1073741824)) return n = d !== null ? d.baseLanes | l : l, r.lanes = r.childLanes = 1073741824, r.memoizedState = { baseLanes: n, cachePool: null, transitions: null }, r.updateQueue = null, xe(ko, Sa), Sa |= n, null;
      r.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, o = d !== null ? d.baseLanes : l, xe(ko, Sa), Sa |= o;
    }
    else d !== null ? (o = d.baseLanes | l, r.memoizedState = null) : o = l, xe(ko, Sa), Sa |= o;
    return sr(n, r, c, l), r.child;
  }
  function Vd(n, r) {
    var l = r.ref;
    (n === null && l !== null || n !== null && n.ref !== l) && (r.flags |= 512, r.flags |= 2097152);
  }
  function qv(n, r, l, o, c) {
    var d = Un(l) ? Kr : Cn.current;
    return d = Xr(r, d), gn(r, c), l = Vl(n, r, l, o, d, c), o = ui(), n !== null && !jn ? (r.updateQueue = n.updateQueue, r.flags &= -2053, n.lanes &= ~c, Fa(n, r, c)) : (pn && o && Mc(r), r.flags |= 1, sr(n, r, l, c), r.child);
  }
  function Kv(n, r, l, o, c) {
    if (Un(l)) {
      var d = !0;
      Jn(r);
    } else d = !1;
    if (gn(r, c), r.stateNode === null) ja(n, r), af(r, l, o), Ds(r, l, o, c), o = !0;
    else if (n === null) {
      var m = r.stateNode, E = r.memoizedProps;
      m.props = E;
      var R = m.context, j = l.contextType;
      typeof j == "object" && j !== null ? j = Aa(j) : (j = Un(l) ? Kr : Cn.current, j = Xr(r, j));
      var W = l.getDerivedStateFromProps, q = typeof W == "function" || typeof m.getSnapshotBeforeUpdate == "function";
      q || typeof m.UNSAFE_componentWillReceiveProps != "function" && typeof m.componentWillReceiveProps != "function" || (E !== o || R !== j) && Qv(r, m, o, j), ga = !1;
      var Q = r.memoizedState;
      m.state = Q, ys(r, o, m, c), R = r.memoizedState, E !== o || Q !== R || Wn.current || ga ? (typeof W == "function" && (zd(r, l, W, o), R = r.memoizedState), (E = ga || Yv(r, l, E, o, Q, R, j)) ? (q || typeof m.UNSAFE_componentWillMount != "function" && typeof m.componentWillMount != "function" || (typeof m.componentWillMount == "function" && m.componentWillMount(), typeof m.UNSAFE_componentWillMount == "function" && m.UNSAFE_componentWillMount()), typeof m.componentDidMount == "function" && (r.flags |= 4194308)) : (typeof m.componentDidMount == "function" && (r.flags |= 4194308), r.memoizedProps = o, r.memoizedState = R), m.props = o, m.state = R, m.context = j, o = E) : (typeof m.componentDidMount == "function" && (r.flags |= 4194308), o = !1);
    } else {
      m = r.stateNode, Pv(n, r), E = r.memoizedProps, j = r.type === r.elementType ? E : oi(r.type, E), m.props = j, q = r.pendingProps, Q = m.context, R = l.contextType, typeof R == "object" && R !== null ? R = Aa(R) : (R = Un(l) ? Kr : Cn.current, R = Xr(r, R));
      var pe = l.getDerivedStateFromProps;
      (W = typeof pe == "function" || typeof m.getSnapshotBeforeUpdate == "function") || typeof m.UNSAFE_componentWillReceiveProps != "function" && typeof m.componentWillReceiveProps != "function" || (E !== q || Q !== R) && Qv(r, m, o, R), ga = !1, Q = r.memoizedState, m.state = Q, ys(r, o, m, c);
      var Se = r.memoizedState;
      E !== q || Q !== Se || Wn.current || ga ? (typeof pe == "function" && (zd(r, l, pe, o), Se = r.memoizedState), (j = ga || Yv(r, l, j, o, Q, Se, R) || !1) ? (W || typeof m.UNSAFE_componentWillUpdate != "function" && typeof m.componentWillUpdate != "function" || (typeof m.componentWillUpdate == "function" && m.componentWillUpdate(o, Se, R), typeof m.UNSAFE_componentWillUpdate == "function" && m.UNSAFE_componentWillUpdate(o, Se, R)), typeof m.componentDidUpdate == "function" && (r.flags |= 4), typeof m.getSnapshotBeforeUpdate == "function" && (r.flags |= 1024)) : (typeof m.componentDidUpdate != "function" || E === n.memoizedProps && Q === n.memoizedState || (r.flags |= 4), typeof m.getSnapshotBeforeUpdate != "function" || E === n.memoizedProps && Q === n.memoizedState || (r.flags |= 1024), r.memoizedProps = o, r.memoizedState = Se), m.props = o, m.state = Se, m.context = R, o = j) : (typeof m.componentDidUpdate != "function" || E === n.memoizedProps && Q === n.memoizedState || (r.flags |= 4), typeof m.getSnapshotBeforeUpdate != "function" || E === n.memoizedProps && Q === n.memoizedState || (r.flags |= 1024), o = !1);
    }
    return Ls(n, r, l, o, d, c);
  }
  function Ls(n, r, l, o, c, d) {
    Vd(n, r);
    var m = (r.flags & 128) !== 0;
    if (!o && !m) return c && Nc(r, l, !1), Fa(n, r, d);
    o = r.stateNode, Os.current = r;
    var E = m && typeof l.getDerivedStateFromError != "function" ? null : o.render();
    return r.flags |= 1, n !== null && m ? (r.child = bn(r, n.child, null, d), r.child = bn(r, null, E, d)) : sr(n, r, E, d), r.memoizedState = o.state, c && Nc(r, l, !0), r.child;
  }
  function wo(n) {
    var r = n.stateNode;
    r.pendingContext ? jv(n, r.pendingContext, r.pendingContext !== r.context) : r.context && jv(n, r.context, !1), Ld(n, r.containerInfo);
  }
  function Xv(n, r, l, o, c) {
    return Fl(), Ji(c), r.flags |= 256, sr(n, r, l, o), r.child;
  }
  var uf = { dehydrated: null, treeContext: null, retryLane: 0 };
  function Pd(n) {
    return { baseLanes: n, cachePool: null, transitions: null };
  }
  function of(n, r, l) {
    var o = r.pendingProps, c = Sn.current, d = !1, m = (r.flags & 128) !== 0, E;
    if ((E = m) || (E = n !== null && n.memoizedState === null ? !1 : (c & 2) !== 0), E ? (d = !0, r.flags &= -129) : (n === null || n.memoizedState !== null) && (c |= 1), xe(Sn, c & 1), n === null)
      return Rd(r), n = r.memoizedState, n !== null && (n = n.dehydrated, n !== null) ? (r.mode & 1 ? n.data === "$!" ? r.lanes = 8 : r.lanes = 1073741824 : r.lanes = 1, null) : (m = o.children, n = o.fallback, d ? (o = r.mode, d = r.child, m = { mode: "hidden", children: m }, !(o & 1) && d !== null ? (d.childLanes = 0, d.pendingProps = m) : d = Wl(m, o, 0, null), n = il(n, o, l, null), d.return = r, n.return = r, d.sibling = n, r.child = d, r.child.memoizedState = Pd(l), r.memoizedState = uf, n) : Bd(r, m));
    if (c = n.memoizedState, c !== null && (E = c.dehydrated, E !== null)) return Zv(n, r, m, o, E, c, l);
    if (d) {
      d = o.fallback, m = r.mode, c = n.child, E = c.sibling;
      var R = { mode: "hidden", children: o.children };
      return !(m & 1) && r.child !== c ? (o = r.child, o.childLanes = 0, o.pendingProps = R, r.deletions = null) : (o = Ql(c, R), o.subtreeFlags = c.subtreeFlags & 14680064), E !== null ? d = Ql(E, d) : (d = il(d, m, l, null), d.flags |= 2), d.return = r, o.return = r, o.sibling = d, r.child = o, o = d, d = r.child, m = n.child.memoizedState, m = m === null ? Pd(l) : { baseLanes: m.baseLanes | l, cachePool: null, transitions: m.transitions }, d.memoizedState = m, d.childLanes = n.childLanes & ~l, r.memoizedState = uf, o;
    }
    return d = n.child, n = d.sibling, o = Ql(d, { mode: "visible", children: o.children }), !(r.mode & 1) && (o.lanes = l), o.return = r, o.sibling = null, n !== null && (l = r.deletions, l === null ? (r.deletions = [n], r.flags |= 16) : l.push(n)), r.child = o, r.memoizedState = null, o;
  }
  function Bd(n, r) {
    return r = Wl({ mode: "visible", children: r }, n.mode, 0, null), r.return = n, n.child = r;
  }
  function Ms(n, r, l, o) {
    return o !== null && Ji(o), bn(r, n.child, null, l), n = Bd(r, r.pendingProps.children), n.flags |= 2, r.memoizedState = null, n;
  }
  function Zv(n, r, l, o, c, d, m) {
    if (l)
      return r.flags & 256 ? (r.flags &= -257, o = Ad(Error(T(422))), Ms(n, r, m, o)) : r.memoizedState !== null ? (r.child = n.child, r.flags |= 128, null) : (d = o.fallback, c = r.mode, o = Wl({ mode: "visible", children: o.children }, c, 0, null), d = il(d, c, m, null), d.flags |= 2, o.return = r, d.return = r, o.sibling = d, r.child = o, r.mode & 1 && bn(r, n.child, null, m), r.child.memoizedState = Pd(m), r.memoizedState = uf, d);
    if (!(r.mode & 1)) return Ms(n, r, m, null);
    if (c.data === "$!") {
      if (o = c.nextSibling && c.nextSibling.dataset, o) var E = o.dgst;
      return o = E, d = Error(T(419)), o = Ad(d, o, void 0), Ms(n, r, m, o);
    }
    if (E = (m & n.childLanes) !== 0, jn || E) {
      if (o = qn, o !== null) {
        switch (m & -m) {
          case 4:
            c = 2;
            break;
          case 16:
            c = 8;
            break;
          case 64:
          case 128:
          case 256:
          case 512:
          case 1024:
          case 2048:
          case 4096:
          case 8192:
          case 16384:
          case 32768:
          case 65536:
          case 131072:
          case 262144:
          case 524288:
          case 1048576:
          case 2097152:
          case 4194304:
          case 8388608:
          case 16777216:
          case 33554432:
          case 67108864:
            c = 32;
            break;
          case 536870912:
            c = 268435456;
            break;
          default:
            c = 0;
        }
        c = c & (o.suspendedLanes | m) ? 0 : c, c !== 0 && c !== d.retryLane && (d.retryLane = c, ya(n, c), Ar(o, n, c, -1));
      }
      return Zd(), o = Ad(Error(T(421))), Ms(n, r, m, o);
    }
    return c.data === "$?" ? (r.flags |= 128, r.child = n.child, r = Ty.bind(null, n), c._reactRetry = r, null) : (n = d.treeContext, Jr = Ti(c.nextSibling), Zr = r, pn = !0, za = null, n !== null && (zn[Ua++] = ki, zn[Ua++] = Di, zn[Ua++] = ha, ki = n.id, Di = n.overflow, ha = r), r = Bd(r, o.children), r.flags |= 4096, r);
  }
  function $d(n, r, l) {
    n.lanes |= r;
    var o = n.alternate;
    o !== null && (o.lanes |= r), xd(n.return, r, l);
  }
  function Mr(n, r, l, o, c) {
    var d = n.memoizedState;
    d === null ? n.memoizedState = { isBackwards: r, rendering: null, renderingStartTime: 0, last: o, tail: l, tailMode: c } : (d.isBackwards = r, d.rendering = null, d.renderingStartTime = 0, d.last = o, d.tail = l, d.tailMode = c);
  }
  function Ni(n, r, l) {
    var o = r.pendingProps, c = o.revealOrder, d = o.tail;
    if (sr(n, r, o.children, l), o = Sn.current, o & 2) o = o & 1 | 2, r.flags |= 128;
    else {
      if (n !== null && n.flags & 128) e: for (n = r.child; n !== null; ) {
        if (n.tag === 13) n.memoizedState !== null && $d(n, l, r);
        else if (n.tag === 19) $d(n, l, r);
        else if (n.child !== null) {
          n.child.return = n, n = n.child;
          continue;
        }
        if (n === r) break e;
        for (; n.sibling === null; ) {
          if (n.return === null || n.return === r) break e;
          n = n.return;
        }
        n.sibling.return = n.return, n = n.sibling;
      }
      o &= 1;
    }
    if (xe(Sn, o), !(r.mode & 1)) r.memoizedState = null;
    else switch (c) {
      case "forwards":
        for (l = r.child, c = null; l !== null; ) n = l.alternate, n !== null && Hc(n) === null && (c = l), l = l.sibling;
        l = c, l === null ? (c = r.child, r.child = null) : (c = l.sibling, l.sibling = null), Mr(r, !1, c, l, d);
        break;
      case "backwards":
        for (l = null, c = r.child, r.child = null; c !== null; ) {
          if (n = c.alternate, n !== null && Hc(n) === null) {
            r.child = c;
            break;
          }
          n = c.sibling, c.sibling = l, l = c, c = n;
        }
        Mr(r, !0, l, null, d);
        break;
      case "together":
        Mr(r, !1, null, null, void 0);
        break;
      default:
        r.memoizedState = null;
    }
    return r.child;
  }
  function ja(n, r) {
    !(r.mode & 1) && n !== null && (n.alternate = null, r.alternate = null, r.flags |= 2);
  }
  function Fa(n, r, l) {
    if (n !== null && (r.dependencies = n.dependencies), Ui |= r.lanes, !(l & r.childLanes)) return null;
    if (n !== null && r.child !== n.child) throw Error(T(153));
    if (r.child !== null) {
      for (n = r.child, l = Ql(n, n.pendingProps), r.child = l, l.return = r; n.sibling !== null; ) n = n.sibling, l = l.sibling = Ql(n, n.pendingProps), l.return = r;
      l.sibling = null;
    }
    return r.child;
  }
  function Us(n, r, l) {
    switch (r.tag) {
      case 3:
        wo(r), Fl();
        break;
      case 5:
        $v(r);
        break;
      case 1:
        Un(r.type) && Jn(r);
        break;
      case 4:
        Ld(r, r.stateNode.containerInfo);
        break;
      case 10:
        var o = r.type._context, c = r.memoizedProps.value;
        xe(ma, o._currentValue), o._currentValue = c;
        break;
      case 13:
        if (o = r.memoizedState, o !== null)
          return o.dehydrated !== null ? (xe(Sn, Sn.current & 1), r.flags |= 128, null) : l & r.child.childLanes ? of(n, r, l) : (xe(Sn, Sn.current & 1), n = Fa(n, r, l), n !== null ? n.sibling : null);
        xe(Sn, Sn.current & 1);
        break;
      case 19:
        if (o = (l & r.childLanes) !== 0, n.flags & 128) {
          if (o) return Ni(n, r, l);
          r.flags |= 128;
        }
        if (c = r.memoizedState, c !== null && (c.rendering = null, c.tail = null, c.lastEffect = null), xe(Sn, Sn.current), o) break;
        return null;
      case 22:
      case 23:
        return r.lanes = 0, Ns(n, r, l);
    }
    return Fa(n, r, l);
  }
  var Ha, Fn, Jv, eh;
  Ha = function(n, r) {
    for (var l = r.child; l !== null; ) {
      if (l.tag === 5 || l.tag === 6) n.appendChild(l.stateNode);
      else if (l.tag !== 4 && l.child !== null) {
        l.child.return = l, l = l.child;
        continue;
      }
      if (l === r) break;
      for (; l.sibling === null; ) {
        if (l.return === null || l.return === r) return;
        l = l.return;
      }
      l.sibling.return = l.return, l = l.sibling;
    }
  }, Fn = function() {
  }, Jv = function(n, r, l, o) {
    var c = n.memoizedProps;
    if (c !== o) {
      n = r.stateNode, wu(Oi.current);
      var d = null;
      switch (l) {
        case "input":
          c = ar(n, c), o = ar(n, o), d = [];
          break;
        case "select":
          c = ie({}, c, { value: void 0 }), o = ie({}, o, { value: void 0 }), d = [];
          break;
        case "textarea":
          c = Yn(n, c), o = Yn(n, o), d = [];
          break;
        default:
          typeof c.onClick != "function" && typeof o.onClick == "function" && (n.onclick = Ll);
      }
      on(l, o);
      var m;
      l = null;
      for (j in c) if (!o.hasOwnProperty(j) && c.hasOwnProperty(j) && c[j] != null) if (j === "style") {
        var E = c[j];
        for (m in E) E.hasOwnProperty(m) && (l || (l = {}), l[m] = "");
      } else j !== "dangerouslySetInnerHTML" && j !== "children" && j !== "suppressContentEditableWarning" && j !== "suppressHydrationWarning" && j !== "autoFocus" && (ke.hasOwnProperty(j) ? d || (d = []) : (d = d || []).push(j, null));
      for (j in o) {
        var R = o[j];
        if (E = c != null ? c[j] : void 0, o.hasOwnProperty(j) && R !== E && (R != null || E != null)) if (j === "style") if (E) {
          for (m in E) !E.hasOwnProperty(m) || R && R.hasOwnProperty(m) || (l || (l = {}), l[m] = "");
          for (m in R) R.hasOwnProperty(m) && E[m] !== R[m] && (l || (l = {}), l[m] = R[m]);
        } else l || (d || (d = []), d.push(
          j,
          l
        )), l = R;
        else j === "dangerouslySetInnerHTML" ? (R = R ? R.__html : void 0, E = E ? E.__html : void 0, R != null && E !== R && (d = d || []).push(j, R)) : j === "children" ? typeof R != "string" && typeof R != "number" || (d = d || []).push(j, "" + R) : j !== "suppressContentEditableWarning" && j !== "suppressHydrationWarning" && (ke.hasOwnProperty(j) ? (R != null && j === "onScroll" && Pt("scroll", n), d || E === R || (d = [])) : (d = d || []).push(j, R));
      }
      l && (d = d || []).push("style", l);
      var j = d;
      (r.updateQueue = j) && (r.flags |= 4);
    }
  }, eh = function(n, r, l, o) {
    l !== o && (r.flags |= 4);
  };
  function zs(n, r) {
    if (!pn) switch (n.tailMode) {
      case "hidden":
        r = n.tail;
        for (var l = null; r !== null; ) r.alternate !== null && (l = r), r = r.sibling;
        l === null ? n.tail = null : l.sibling = null;
        break;
      case "collapsed":
        l = n.tail;
        for (var o = null; l !== null; ) l.alternate !== null && (o = l), l = l.sibling;
        o === null ? r || n.tail === null ? n.tail = null : n.tail.sibling = null : o.sibling = null;
    }
  }
  function tr(n) {
    var r = n.alternate !== null && n.alternate.child === n.child, l = 0, o = 0;
    if (r) for (var c = n.child; c !== null; ) l |= c.lanes | c.childLanes, o |= c.subtreeFlags & 14680064, o |= c.flags & 14680064, c.return = n, c = c.sibling;
    else for (c = n.child; c !== null; ) l |= c.lanes | c.childLanes, o |= c.subtreeFlags, o |= c.flags, c.return = n, c = c.sibling;
    return n.subtreeFlags |= o, n.childLanes = l, r;
  }
  function th(n, r, l) {
    var o = r.pendingProps;
    switch (Uc(r), r.tag) {
      case 2:
      case 16:
      case 15:
      case 0:
      case 11:
      case 7:
      case 8:
      case 12:
      case 9:
      case 14:
        return tr(r), null;
      case 1:
        return Un(r.type) && Co(), tr(r), null;
      case 3:
        return o = r.stateNode, xu(), an(Wn), an(Cn), Ne(), o.pendingContext && (o.context = o.pendingContext, o.pendingContext = null), (n === null || n.child === null) && (zc(r) ? r.flags |= 4 : n === null || n.memoizedState.isDehydrated && !(r.flags & 256) || (r.flags |= 1024, za !== null && (Fu(za), za = null))), Fn(n, r), tr(r), null;
      case 5:
        Fc(r);
        var c = wu(Es.current);
        if (l = r.type, n !== null && r.stateNode != null) Jv(n, r, l, o, c), n.ref !== r.ref && (r.flags |= 512, r.flags |= 2097152);
        else {
          if (!o) {
            if (r.stateNode === null) throw Error(T(166));
            return tr(r), null;
          }
          if (n = wu(Oi.current), zc(r)) {
            o = r.stateNode, l = r.type;
            var d = r.memoizedProps;
            switch (o[bi] = r, o[ps] = d, n = (r.mode & 1) !== 0, l) {
              case "dialog":
                Pt("cancel", o), Pt("close", o);
                break;
              case "iframe":
              case "object":
              case "embed":
                Pt("load", o);
                break;
              case "video":
              case "audio":
                for (c = 0; c < cs.length; c++) Pt(cs[c], o);
                break;
              case "source":
                Pt("error", o);
                break;
              case "img":
              case "image":
              case "link":
                Pt(
                  "error",
                  o
                ), Pt("load", o);
                break;
              case "details":
                Pt("toggle", o);
                break;
              case "input":
                $n(o, d), Pt("invalid", o);
                break;
              case "select":
                o._wrapperState = { wasMultiple: !!d.multiple }, Pt("invalid", o);
                break;
              case "textarea":
                Er(o, d), Pt("invalid", o);
            }
            on(l, d), c = null;
            for (var m in d) if (d.hasOwnProperty(m)) {
              var E = d[m];
              m === "children" ? typeof E == "string" ? o.textContent !== E && (d.suppressHydrationWarning !== !0 && xc(o.textContent, E, n), c = ["children", E]) : typeof E == "number" && o.textContent !== "" + E && (d.suppressHydrationWarning !== !0 && xc(
                o.textContent,
                E,
                n
              ), c = ["children", "" + E]) : ke.hasOwnProperty(m) && E != null && m === "onScroll" && Pt("scroll", o);
            }
            switch (l) {
              case "input":
                Nn(o), vi(o, d, !0);
                break;
              case "textarea":
                Nn(o), Ln(o);
                break;
              case "select":
              case "option":
                break;
              default:
                typeof d.onClick == "function" && (o.onclick = Ll);
            }
            o = c, r.updateQueue = o, o !== null && (r.flags |= 4);
          } else {
            m = c.nodeType === 9 ? c : c.ownerDocument, n === "http://www.w3.org/1999/xhtml" && (n = Cr(l)), n === "http://www.w3.org/1999/xhtml" ? l === "script" ? (n = m.createElement("div"), n.innerHTML = "<script><\/script>", n = n.removeChild(n.firstChild)) : typeof o.is == "string" ? n = m.createElement(l, { is: o.is }) : (n = m.createElement(l), l === "select" && (m = n, o.multiple ? m.multiple = !0 : o.size && (m.size = o.size))) : n = m.createElementNS(n, l), n[bi] = r, n[ps] = o, Ha(n, r, !1, !1), r.stateNode = n;
            e: {
              switch (m = Zn(l, o), l) {
                case "dialog":
                  Pt("cancel", n), Pt("close", n), c = o;
                  break;
                case "iframe":
                case "object":
                case "embed":
                  Pt("load", n), c = o;
                  break;
                case "video":
                case "audio":
                  for (c = 0; c < cs.length; c++) Pt(cs[c], n);
                  c = o;
                  break;
                case "source":
                  Pt("error", n), c = o;
                  break;
                case "img":
                case "image":
                case "link":
                  Pt(
                    "error",
                    n
                  ), Pt("load", n), c = o;
                  break;
                case "details":
                  Pt("toggle", n), c = o;
                  break;
                case "input":
                  $n(n, o), c = ar(n, o), Pt("invalid", n);
                  break;
                case "option":
                  c = o;
                  break;
                case "select":
                  n._wrapperState = { wasMultiple: !!o.multiple }, c = ie({}, o, { value: void 0 }), Pt("invalid", n);
                  break;
                case "textarea":
                  Er(n, o), c = Yn(n, o), Pt("invalid", n);
                  break;
                default:
                  c = o;
              }
              on(l, c), E = c;
              for (d in E) if (E.hasOwnProperty(d)) {
                var R = E[d];
                d === "style" ? en(n, R) : d === "dangerouslySetInnerHTML" ? (R = R ? R.__html : void 0, R != null && hi(n, R)) : d === "children" ? typeof R == "string" ? (l !== "textarea" || R !== "") && re(n, R) : typeof R == "number" && re(n, "" + R) : d !== "suppressContentEditableWarning" && d !== "suppressHydrationWarning" && d !== "autoFocus" && (ke.hasOwnProperty(d) ? R != null && d === "onScroll" && Pt("scroll", n) : R != null && Ke(n, d, R, m));
              }
              switch (l) {
                case "input":
                  Nn(n), vi(n, o, !1);
                  break;
                case "textarea":
                  Nn(n), Ln(n);
                  break;
                case "option":
                  o.value != null && n.setAttribute("value", "" + at(o.value));
                  break;
                case "select":
                  n.multiple = !!o.multiple, d = o.value, d != null ? Rn(n, !!o.multiple, d, !1) : o.defaultValue != null && Rn(
                    n,
                    !!o.multiple,
                    o.defaultValue,
                    !0
                  );
                  break;
                default:
                  typeof c.onClick == "function" && (n.onclick = Ll);
              }
              switch (l) {
                case "button":
                case "input":
                case "select":
                case "textarea":
                  o = !!o.autoFocus;
                  break e;
                case "img":
                  o = !0;
                  break e;
                default:
                  o = !1;
              }
            }
            o && (r.flags |= 4);
          }
          r.ref !== null && (r.flags |= 512, r.flags |= 2097152);
        }
        return tr(r), null;
      case 6:
        if (n && r.stateNode != null) eh(n, r, n.memoizedProps, o);
        else {
          if (typeof o != "string" && r.stateNode === null) throw Error(T(166));
          if (l = wu(Es.current), wu(Oi.current), zc(r)) {
            if (o = r.stateNode, l = r.memoizedProps, o[bi] = r, (d = o.nodeValue !== l) && (n = Zr, n !== null)) switch (n.tag) {
              case 3:
                xc(o.nodeValue, l, (n.mode & 1) !== 0);
                break;
              case 5:
                n.memoizedProps.suppressHydrationWarning !== !0 && xc(o.nodeValue, l, (n.mode & 1) !== 0);
            }
            d && (r.flags |= 4);
          } else o = (l.nodeType === 9 ? l : l.ownerDocument).createTextNode(o), o[bi] = r, r.stateNode = o;
        }
        return tr(r), null;
      case 13:
        if (an(Sn), o = r.memoizedState, n === null || n.memoizedState !== null && n.memoizedState.dehydrated !== null) {
          if (pn && Jr !== null && r.mode & 1 && !(r.flags & 128)) ms(), Fl(), r.flags |= 98560, d = !1;
          else if (d = zc(r), o !== null && o.dehydrated !== null) {
            if (n === null) {
              if (!d) throw Error(T(318));
              if (d = r.memoizedState, d = d !== null ? d.dehydrated : null, !d) throw Error(T(317));
              d[bi] = r;
            } else Fl(), !(r.flags & 128) && (r.memoizedState = null), r.flags |= 4;
            tr(r), d = !1;
          } else za !== null && (Fu(za), za = null), d = !0;
          if (!d) return r.flags & 65536 ? r : null;
        }
        return r.flags & 128 ? (r.lanes = l, r) : (o = o !== null, o !== (n !== null && n.memoizedState !== null) && o && (r.child.flags |= 8192, r.mode & 1 && (n === null || Sn.current & 1 ? kn === 0 && (kn = 3) : Zd())), r.updateQueue !== null && (r.flags |= 4), tr(r), null);
      case 4:
        return xu(), Fn(n, r), n === null && mo(r.stateNode.containerInfo), tr(r), null;
      case 10:
        return wd(r.type._context), tr(r), null;
      case 17:
        return Un(r.type) && Co(), tr(r), null;
      case 19:
        if (an(Sn), d = r.memoizedState, d === null) return tr(r), null;
        if (o = (r.flags & 128) !== 0, m = d.rendering, m === null) if (o) zs(d, !1);
        else {
          if (kn !== 0 || n !== null && n.flags & 128) for (n = r.child; n !== null; ) {
            if (m = Hc(n), m !== null) {
              for (r.flags |= 128, zs(d, !1), o = m.updateQueue, o !== null && (r.updateQueue = o, r.flags |= 4), r.subtreeFlags = 0, o = l, l = r.child; l !== null; ) d = l, n = o, d.flags &= 14680066, m = d.alternate, m === null ? (d.childLanes = 0, d.lanes = n, d.child = null, d.subtreeFlags = 0, d.memoizedProps = null, d.memoizedState = null, d.updateQueue = null, d.dependencies = null, d.stateNode = null) : (d.childLanes = m.childLanes, d.lanes = m.lanes, d.child = m.child, d.subtreeFlags = 0, d.deletions = null, d.memoizedProps = m.memoizedProps, d.memoizedState = m.memoizedState, d.updateQueue = m.updateQueue, d.type = m.type, n = m.dependencies, d.dependencies = n === null ? null : { lanes: n.lanes, firstContext: n.firstContext }), l = l.sibling;
              return xe(Sn, Sn.current & 1 | 2), r.child;
            }
            n = n.sibling;
          }
          d.tail !== null && Je() > Oo && (r.flags |= 128, o = !0, zs(d, !1), r.lanes = 4194304);
        }
        else {
          if (!o) if (n = Hc(m), n !== null) {
            if (r.flags |= 128, o = !0, l = n.updateQueue, l !== null && (r.updateQueue = l, r.flags |= 4), zs(d, !0), d.tail === null && d.tailMode === "hidden" && !m.alternate && !pn) return tr(r), null;
          } else 2 * Je() - d.renderingStartTime > Oo && l !== 1073741824 && (r.flags |= 128, o = !0, zs(d, !1), r.lanes = 4194304);
          d.isBackwards ? (m.sibling = r.child, r.child = m) : (l = d.last, l !== null ? l.sibling = m : r.child = m, d.last = m);
        }
        return d.tail !== null ? (r = d.tail, d.rendering = r, d.tail = r.sibling, d.renderingStartTime = Je(), r.sibling = null, l = Sn.current, xe(Sn, o ? l & 1 | 2 : l & 1), r) : (tr(r), null);
      case 22:
      case 23:
        return Xd(), o = r.memoizedState !== null, n !== null && n.memoizedState !== null !== o && (r.flags |= 8192), o && r.mode & 1 ? Sa & 1073741824 && (tr(r), r.subtreeFlags & 6 && (r.flags |= 8192)) : tr(r), null;
      case 24:
        return null;
      case 25:
        return null;
    }
    throw Error(T(156, r.tag));
  }
  function sf(n, r) {
    switch (Uc(r), r.tag) {
      case 1:
        return Un(r.type) && Co(), n = r.flags, n & 65536 ? (r.flags = n & -65537 | 128, r) : null;
      case 3:
        return xu(), an(Wn), an(Cn), Ne(), n = r.flags, n & 65536 && !(n & 128) ? (r.flags = n & -65537 | 128, r) : null;
      case 5:
        return Fc(r), null;
      case 13:
        if (an(Sn), n = r.memoizedState, n !== null && n.dehydrated !== null) {
          if (r.alternate === null) throw Error(T(340));
          Fl();
        }
        return n = r.flags, n & 65536 ? (r.flags = n & -65537 | 128, r) : null;
      case 19:
        return an(Sn), null;
      case 4:
        return xu(), null;
      case 10:
        return wd(r.type._context), null;
      case 22:
      case 23:
        return Xd(), null;
      case 24:
        return null;
      default:
        return null;
    }
  }
  var As = !1, br = !1, yy = typeof WeakSet == "function" ? WeakSet : Set, ye = null;
  function xo(n, r) {
    var l = n.ref;
    if (l !== null) if (typeof l == "function") try {
      l(null);
    } catch (o) {
      vn(n, r, o);
    }
    else l.current = null;
  }
  function cf(n, r, l) {
    try {
      l();
    } catch (o) {
      vn(n, r, o);
    }
  }
  var nh = !1;
  function rh(n, r) {
    if (ds = Oa, n = os(), Sc(n)) {
      if ("selectionStart" in n) var l = { start: n.selectionStart, end: n.selectionEnd };
      else e: {
        l = (l = n.ownerDocument) && l.defaultView || window;
        var o = l.getSelection && l.getSelection();
        if (o && o.rangeCount !== 0) {
          l = o.anchorNode;
          var c = o.anchorOffset, d = o.focusNode;
          o = o.focusOffset;
          try {
            l.nodeType, d.nodeType;
          } catch {
            l = null;
            break e;
          }
          var m = 0, E = -1, R = -1, j = 0, W = 0, q = n, Q = null;
          t: for (; ; ) {
            for (var pe; q !== l || c !== 0 && q.nodeType !== 3 || (E = m + c), q !== d || o !== 0 && q.nodeType !== 3 || (R = m + o), q.nodeType === 3 && (m += q.nodeValue.length), (pe = q.firstChild) !== null; )
              Q = q, q = pe;
            for (; ; ) {
              if (q === n) break t;
              if (Q === l && ++j === c && (E = m), Q === d && ++W === o && (R = m), (pe = q.nextSibling) !== null) break;
              q = Q, Q = q.parentNode;
            }
            q = pe;
          }
          l = E === -1 || R === -1 ? null : { start: E, end: R };
        } else l = null;
      }
      l = l || { start: 0, end: 0 };
    } else l = null;
    for (Eu = { focusedElem: n, selectionRange: l }, Oa = !1, ye = r; ye !== null; ) if (r = ye, n = r.child, (r.subtreeFlags & 1028) !== 0 && n !== null) n.return = r, ye = n;
    else for (; ye !== null; ) {
      r = ye;
      try {
        var Se = r.alternate;
        if (r.flags & 1024) switch (r.tag) {
          case 0:
          case 11:
          case 15:
            break;
          case 1:
            if (Se !== null) {
              var _e = Se.memoizedProps, Dn = Se.memoizedState, D = r.stateNode, w = D.getSnapshotBeforeUpdate(r.elementType === r.type ? _e : oi(r.type, _e), Dn);
              D.__reactInternalSnapshotBeforeUpdate = w;
            }
            break;
          case 3:
            var M = r.stateNode.containerInfo;
            M.nodeType === 1 ? M.textContent = "" : M.nodeType === 9 && M.documentElement && M.removeChild(M.documentElement);
            break;
          case 5:
          case 6:
          case 4:
          case 17:
            break;
          default:
            throw Error(T(163));
        }
      } catch (G) {
        vn(r, r.return, G);
      }
      if (n = r.sibling, n !== null) {
        n.return = r.return, ye = n;
        break;
      }
      ye = r.return;
    }
    return Se = nh, nh = !1, Se;
  }
  function js(n, r, l) {
    var o = r.updateQueue;
    if (o = o !== null ? o.lastEffect : null, o !== null) {
      var c = o = o.next;
      do {
        if ((c.tag & n) === n) {
          var d = c.destroy;
          c.destroy = void 0, d !== void 0 && cf(r, l, d);
        }
        c = c.next;
      } while (c !== o);
    }
  }
  function Fs(n, r) {
    if (r = r.updateQueue, r = r !== null ? r.lastEffect : null, r !== null) {
      var l = r = r.next;
      do {
        if ((l.tag & n) === n) {
          var o = l.create;
          l.destroy = o();
        }
        l = l.next;
      } while (l !== r);
    }
  }
  function Id(n) {
    var r = n.ref;
    if (r !== null) {
      var l = n.stateNode;
      switch (n.tag) {
        case 5:
          n = l;
          break;
        default:
          n = l;
      }
      typeof r == "function" ? r(n) : r.current = n;
    }
  }
  function ff(n) {
    var r = n.alternate;
    r !== null && (n.alternate = null, ff(r)), n.child = null, n.deletions = null, n.sibling = null, n.tag === 5 && (r = n.stateNode, r !== null && (delete r[bi], delete r[ps], delete r[vs], delete r[Eo], delete r[hy])), n.stateNode = null, n.return = null, n.dependencies = null, n.memoizedProps = null, n.memoizedState = null, n.pendingProps = null, n.stateNode = null, n.updateQueue = null;
  }
  function Hs(n) {
    return n.tag === 5 || n.tag === 3 || n.tag === 4;
  }
  function nl(n) {
    e: for (; ; ) {
      for (; n.sibling === null; ) {
        if (n.return === null || Hs(n.return)) return null;
        n = n.return;
      }
      for (n.sibling.return = n.return, n = n.sibling; n.tag !== 5 && n.tag !== 6 && n.tag !== 18; ) {
        if (n.flags & 2 || n.child === null || n.tag === 4) continue e;
        n.child.return = n, n = n.child;
      }
      if (!(n.flags & 2)) return n.stateNode;
    }
  }
  function Li(n, r, l) {
    var o = n.tag;
    if (o === 5 || o === 6) n = n.stateNode, r ? l.nodeType === 8 ? l.parentNode.insertBefore(n, r) : l.insertBefore(n, r) : (l.nodeType === 8 ? (r = l.parentNode, r.insertBefore(n, l)) : (r = l, r.appendChild(n)), l = l._reactRootContainer, l != null || r.onclick !== null || (r.onclick = Ll));
    else if (o !== 4 && (n = n.child, n !== null)) for (Li(n, r, l), n = n.sibling; n !== null; ) Li(n, r, l), n = n.sibling;
  }
  function Mi(n, r, l) {
    var o = n.tag;
    if (o === 5 || o === 6) n = n.stateNode, r ? l.insertBefore(n, r) : l.appendChild(n);
    else if (o !== 4 && (n = n.child, n !== null)) for (Mi(n, r, l), n = n.sibling; n !== null; ) Mi(n, r, l), n = n.sibling;
  }
  var xn = null, Ur = !1;
  function zr(n, r, l) {
    for (l = l.child; l !== null; ) ah(n, r, l), l = l.sibling;
  }
  function ah(n, r, l) {
    if (Gr && typeof Gr.onCommitFiberUnmount == "function") try {
      Gr.onCommitFiberUnmount(Rl, l);
    } catch {
    }
    switch (l.tag) {
      case 5:
        br || xo(l, r);
      case 6:
        var o = xn, c = Ur;
        xn = null, zr(n, r, l), xn = o, Ur = c, xn !== null && (Ur ? (n = xn, l = l.stateNode, n.nodeType === 8 ? n.parentNode.removeChild(l) : n.removeChild(l)) : xn.removeChild(l.stateNode));
        break;
      case 18:
        xn !== null && (Ur ? (n = xn, l = l.stateNode, n.nodeType === 8 ? So(n.parentNode, l) : n.nodeType === 1 && So(n, l), ri(n)) : So(xn, l.stateNode));
        break;
      case 4:
        o = xn, c = Ur, xn = l.stateNode.containerInfo, Ur = !0, zr(n, r, l), xn = o, Ur = c;
        break;
      case 0:
      case 11:
      case 14:
      case 15:
        if (!br && (o = l.updateQueue, o !== null && (o = o.lastEffect, o !== null))) {
          c = o = o.next;
          do {
            var d = c, m = d.destroy;
            d = d.tag, m !== void 0 && (d & 2 || d & 4) && cf(l, r, m), c = c.next;
          } while (c !== o);
        }
        zr(n, r, l);
        break;
      case 1:
        if (!br && (xo(l, r), o = l.stateNode, typeof o.componentWillUnmount == "function")) try {
          o.props = l.memoizedProps, o.state = l.memoizedState, o.componentWillUnmount();
        } catch (E) {
          vn(l, r, E);
        }
        zr(n, r, l);
        break;
      case 21:
        zr(n, r, l);
        break;
      case 22:
        l.mode & 1 ? (br = (o = br) || l.memoizedState !== null, zr(n, r, l), br = o) : zr(n, r, l);
        break;
      default:
        zr(n, r, l);
    }
  }
  function ih(n) {
    var r = n.updateQueue;
    if (r !== null) {
      n.updateQueue = null;
      var l = n.stateNode;
      l === null && (l = n.stateNode = new yy()), r.forEach(function(o) {
        var c = vh.bind(null, n, o);
        l.has(o) || (l.add(o), o.then(c, c));
      });
    }
  }
  function si(n, r) {
    var l = r.deletions;
    if (l !== null) for (var o = 0; o < l.length; o++) {
      var c = l[o];
      try {
        var d = n, m = r, E = m;
        e: for (; E !== null; ) {
          switch (E.tag) {
            case 5:
              xn = E.stateNode, Ur = !1;
              break e;
            case 3:
              xn = E.stateNode.containerInfo, Ur = !0;
              break e;
            case 4:
              xn = E.stateNode.containerInfo, Ur = !0;
              break e;
          }
          E = E.return;
        }
        if (xn === null) throw Error(T(160));
        ah(d, m, c), xn = null, Ur = !1;
        var R = c.alternate;
        R !== null && (R.return = null), c.return = null;
      } catch (j) {
        vn(c, r, j);
      }
    }
    if (r.subtreeFlags & 12854) for (r = r.child; r !== null; ) Yd(r, n), r = r.sibling;
  }
  function Yd(n, r) {
    var l = n.alternate, o = n.flags;
    switch (n.tag) {
      case 0:
      case 11:
      case 14:
      case 15:
        if (si(r, n), ra(n), o & 4) {
          try {
            js(3, n, n.return), Fs(3, n);
          } catch (_e) {
            vn(n, n.return, _e);
          }
          try {
            js(5, n, n.return);
          } catch (_e) {
            vn(n, n.return, _e);
          }
        }
        break;
      case 1:
        si(r, n), ra(n), o & 512 && l !== null && xo(l, l.return);
        break;
      case 5:
        if (si(r, n), ra(n), o & 512 && l !== null && xo(l, l.return), n.flags & 32) {
          var c = n.stateNode;
          try {
            re(c, "");
          } catch (_e) {
            vn(n, n.return, _e);
          }
        }
        if (o & 4 && (c = n.stateNode, c != null)) {
          var d = n.memoizedProps, m = l !== null ? l.memoizedProps : d, E = n.type, R = n.updateQueue;
          if (n.updateQueue = null, R !== null) try {
            E === "input" && d.type === "radio" && d.name != null && In(c, d), Zn(E, m);
            var j = Zn(E, d);
            for (m = 0; m < R.length; m += 2) {
              var W = R[m], q = R[m + 1];
              W === "style" ? en(c, q) : W === "dangerouslySetInnerHTML" ? hi(c, q) : W === "children" ? re(c, q) : Ke(c, W, q, j);
            }
            switch (E) {
              case "input":
                Wr(c, d);
                break;
              case "textarea":
                qa(c, d);
                break;
              case "select":
                var Q = c._wrapperState.wasMultiple;
                c._wrapperState.wasMultiple = !!d.multiple;
                var pe = d.value;
                pe != null ? Rn(c, !!d.multiple, pe, !1) : Q !== !!d.multiple && (d.defaultValue != null ? Rn(
                  c,
                  !!d.multiple,
                  d.defaultValue,
                  !0
                ) : Rn(c, !!d.multiple, d.multiple ? [] : "", !1));
            }
            c[ps] = d;
          } catch (_e) {
            vn(n, n.return, _e);
          }
        }
        break;
      case 6:
        if (si(r, n), ra(n), o & 4) {
          if (n.stateNode === null) throw Error(T(162));
          c = n.stateNode, d = n.memoizedProps;
          try {
            c.nodeValue = d;
          } catch (_e) {
            vn(n, n.return, _e);
          }
        }
        break;
      case 3:
        if (si(r, n), ra(n), o & 4 && l !== null && l.memoizedState.isDehydrated) try {
          ri(r.containerInfo);
        } catch (_e) {
          vn(n, n.return, _e);
        }
        break;
      case 4:
        si(r, n), ra(n);
        break;
      case 13:
        si(r, n), ra(n), c = n.child, c.flags & 8192 && (d = c.memoizedState !== null, c.stateNode.isHidden = d, !d || c.alternate !== null && c.alternate.memoizedState !== null || (Gd = Je())), o & 4 && ih(n);
        break;
      case 22:
        if (W = l !== null && l.memoizedState !== null, n.mode & 1 ? (br = (j = br) || W, si(r, n), br = j) : si(r, n), ra(n), o & 8192) {
          if (j = n.memoizedState !== null, (n.stateNode.isHidden = j) && !W && n.mode & 1) for (ye = n, W = n.child; W !== null; ) {
            for (q = ye = W; ye !== null; ) {
              switch (Q = ye, pe = Q.child, Q.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  js(4, Q, Q.return);
                  break;
                case 1:
                  xo(Q, Q.return);
                  var Se = Q.stateNode;
                  if (typeof Se.componentWillUnmount == "function") {
                    o = Q, l = Q.return;
                    try {
                      r = o, Se.props = r.memoizedProps, Se.state = r.memoizedState, Se.componentWillUnmount();
                    } catch (_e) {
                      vn(o, l, _e);
                    }
                  }
                  break;
                case 5:
                  xo(Q, Q.return);
                  break;
                case 22:
                  if (Q.memoizedState !== null) {
                    Vs(q);
                    continue;
                  }
              }
              pe !== null ? (pe.return = Q, ye = pe) : Vs(q);
            }
            W = W.sibling;
          }
          e: for (W = null, q = n; ; ) {
            if (q.tag === 5) {
              if (W === null) {
                W = q;
                try {
                  c = q.stateNode, j ? (d = c.style, typeof d.setProperty == "function" ? d.setProperty("display", "none", "important") : d.display = "none") : (E = q.stateNode, R = q.memoizedProps.style, m = R != null && R.hasOwnProperty("display") ? R.display : null, E.style.display = Ht("display", m));
                } catch (_e) {
                  vn(n, n.return, _e);
                }
              }
            } else if (q.tag === 6) {
              if (W === null) try {
                q.stateNode.nodeValue = j ? "" : q.memoizedProps;
              } catch (_e) {
                vn(n, n.return, _e);
              }
            } else if ((q.tag !== 22 && q.tag !== 23 || q.memoizedState === null || q === n) && q.child !== null) {
              q.child.return = q, q = q.child;
              continue;
            }
            if (q === n) break e;
            for (; q.sibling === null; ) {
              if (q.return === null || q.return === n) break e;
              W === q && (W = null), q = q.return;
            }
            W === q && (W = null), q.sibling.return = q.return, q = q.sibling;
          }
        }
        break;
      case 19:
        si(r, n), ra(n), o & 4 && ih(n);
        break;
      case 21:
        break;
      default:
        si(
          r,
          n
        ), ra(n);
    }
  }
  function ra(n) {
    var r = n.flags;
    if (r & 2) {
      try {
        e: {
          for (var l = n.return; l !== null; ) {
            if (Hs(l)) {
              var o = l;
              break e;
            }
            l = l.return;
          }
          throw Error(T(160));
        }
        switch (o.tag) {
          case 5:
            var c = o.stateNode;
            o.flags & 32 && (re(c, ""), o.flags &= -33);
            var d = nl(n);
            Mi(n, d, c);
            break;
          case 3:
          case 4:
            var m = o.stateNode.containerInfo, E = nl(n);
            Li(n, E, m);
            break;
          default:
            throw Error(T(161));
        }
      } catch (R) {
        vn(n, n.return, R);
      }
      n.flags &= -3;
    }
    r & 4096 && (n.flags &= -4097);
  }
  function gy(n, r, l) {
    ye = n, Qd(n);
  }
  function Qd(n, r, l) {
    for (var o = (n.mode & 1) !== 0; ye !== null; ) {
      var c = ye, d = c.child;
      if (c.tag === 22 && o) {
        var m = c.memoizedState !== null || As;
        if (!m) {
          var E = c.alternate, R = E !== null && E.memoizedState !== null || br;
          E = As;
          var j = br;
          if (As = m, (br = R) && !j) for (ye = c; ye !== null; ) m = ye, R = m.child, m.tag === 22 && m.memoizedState !== null ? Wd(c) : R !== null ? (R.return = m, ye = R) : Wd(c);
          for (; d !== null; ) ye = d, Qd(d), d = d.sibling;
          ye = c, As = E, br = j;
        }
        lh(n);
      } else c.subtreeFlags & 8772 && d !== null ? (d.return = c, ye = d) : lh(n);
    }
  }
  function lh(n) {
    for (; ye !== null; ) {
      var r = ye;
      if (r.flags & 8772) {
        var l = r.alternate;
        try {
          if (r.flags & 8772) switch (r.tag) {
            case 0:
            case 11:
            case 15:
              br || Fs(5, r);
              break;
            case 1:
              var o = r.stateNode;
              if (r.flags & 4 && !br) if (l === null) o.componentDidMount();
              else {
                var c = r.elementType === r.type ? l.memoizedProps : oi(r.type, l.memoizedProps);
                o.componentDidUpdate(c, l.memoizedState, o.__reactInternalSnapshotBeforeUpdate);
              }
              var d = r.updateQueue;
              d !== null && Nd(r, d, o);
              break;
            case 3:
              var m = r.updateQueue;
              if (m !== null) {
                if (l = null, r.child !== null) switch (r.child.tag) {
                  case 5:
                    l = r.child.stateNode;
                    break;
                  case 1:
                    l = r.child.stateNode;
                }
                Nd(r, m, l);
              }
              break;
            case 5:
              var E = r.stateNode;
              if (l === null && r.flags & 4) {
                l = E;
                var R = r.memoizedProps;
                switch (r.type) {
                  case "button":
                  case "input":
                  case "select":
                  case "textarea":
                    R.autoFocus && l.focus();
                    break;
                  case "img":
                    R.src && (l.src = R.src);
                }
              }
              break;
            case 6:
              break;
            case 4:
              break;
            case 12:
              break;
            case 13:
              if (r.memoizedState === null) {
                var j = r.alternate;
                if (j !== null) {
                  var W = j.memoizedState;
                  if (W !== null) {
                    var q = W.dehydrated;
                    q !== null && ri(q);
                  }
                }
              }
              break;
            case 19:
            case 17:
            case 21:
            case 22:
            case 23:
            case 25:
              break;
            default:
              throw Error(T(163));
          }
          br || r.flags & 512 && Id(r);
        } catch (Q) {
          vn(r, r.return, Q);
        }
      }
      if (r === n) {
        ye = null;
        break;
      }
      if (l = r.sibling, l !== null) {
        l.return = r.return, ye = l;
        break;
      }
      ye = r.return;
    }
  }
  function Vs(n) {
    for (; ye !== null; ) {
      var r = ye;
      if (r === n) {
        ye = null;
        break;
      }
      var l = r.sibling;
      if (l !== null) {
        l.return = r.return, ye = l;
        break;
      }
      ye = r.return;
    }
  }
  function Wd(n) {
    for (; ye !== null; ) {
      var r = ye;
      try {
        switch (r.tag) {
          case 0:
          case 11:
          case 15:
            var l = r.return;
            try {
              Fs(4, r);
            } catch (R) {
              vn(r, l, R);
            }
            break;
          case 1:
            var o = r.stateNode;
            if (typeof o.componentDidMount == "function") {
              var c = r.return;
              try {
                o.componentDidMount();
              } catch (R) {
                vn(r, c, R);
              }
            }
            var d = r.return;
            try {
              Id(r);
            } catch (R) {
              vn(r, d, R);
            }
            break;
          case 5:
            var m = r.return;
            try {
              Id(r);
            } catch (R) {
              vn(r, m, R);
            }
        }
      } catch (R) {
        vn(r, r.return, R);
      }
      if (r === n) {
        ye = null;
        break;
      }
      var E = r.sibling;
      if (E !== null) {
        E.return = r.return, ye = E;
        break;
      }
      ye = r.return;
    }
  }
  var Sy = Math.ceil, $l = yt.ReactCurrentDispatcher, Au = yt.ReactCurrentOwner, cr = yt.ReactCurrentBatchConfig, _t = 0, qn = null, Hn = null, fr = 0, Sa = 0, ko = Ma(0), kn = 0, Ps = null, Ui = 0, Do = 0, df = 0, Bs = null, aa = null, Gd = 0, Oo = 1 / 0, Ea = null, No = !1, ju = null, Il = null, pf = !1, rl = null, $s = 0, Yl = 0, Lo = null, Is = -1, wr = 0;
  function Vn() {
    return _t & 6 ? Je() : Is !== -1 ? Is : Is = Je();
  }
  function zi(n) {
    return n.mode & 1 ? _t & 2 && fr !== 0 ? fr & -fr : my.transition !== null ? (wr === 0 && (wr = ro()), wr) : (n = Lt, n !== 0 || (n = window.event, n = n === void 0 ? 16 : co(n.type)), n) : 1;
  }
  function Ar(n, r, l, o) {
    if (50 < Yl) throw Yl = 0, Lo = null, Error(T(185));
    Ii(n, l, o), (!(_t & 2) || n !== qn) && (n === qn && (!(_t & 2) && (Do |= l), kn === 4 && ci(n, fr)), ia(n, o), l === 1 && _t === 0 && !(r.mode & 1) && (Oo = Je() + 500, _o && xi()));
  }
  function ia(n, r) {
    var l = n.callbackNode;
    fu(n, r);
    var o = ni(n, n === qn ? fr : 0);
    if (o === 0) l !== null && lr(l), n.callbackNode = null, n.callbackPriority = 0;
    else if (r = o & -o, n.callbackPriority !== r) {
      if (l != null && lr(l), r === 1) n.tag === 0 ? Ul(qd.bind(null, n)) : Lc(qd.bind(null, n)), go(function() {
        !(_t & 6) && xi();
      }), l = null;
      else {
        switch (io(o)) {
          case 1:
            l = ei;
            break;
          case 4:
            l = su;
            break;
          case 16:
            l = cu;
            break;
          case 536870912:
            l = eo;
            break;
          default:
            l = cu;
        }
        l = mh(l, vf.bind(null, n));
      }
      n.callbackPriority = r, n.callbackNode = l;
    }
  }
  function vf(n, r) {
    if (Is = -1, wr = 0, _t & 6) throw Error(T(327));
    var l = n.callbackNode;
    if (Mo() && n.callbackNode !== l) return null;
    var o = ni(n, n === qn ? fr : 0);
    if (o === 0) return null;
    if (o & 30 || o & n.expiredLanes || r) r = hf(n, o);
    else {
      r = o;
      var c = _t;
      _t |= 2;
      var d = oh();
      (qn !== n || fr !== r) && (Ea = null, Oo = Je() + 500, al(n, r));
      do
        try {
          sh();
          break;
        } catch (E) {
          uh(n, E);
        }
      while (!0);
      bd(), $l.current = d, _t = c, Hn !== null ? r = 0 : (qn = null, fr = 0, r = kn);
    }
    if (r !== 0) {
      if (r === 2 && (c = bl(n), c !== 0 && (o = c, r = Ys(n, c))), r === 1) throw l = Ps, al(n, 0), ci(n, o), ia(n, Je()), l;
      if (r === 6) ci(n, o);
      else {
        if (c = n.current.alternate, !(o & 30) && !Ey(c) && (r = hf(n, o), r === 2 && (d = bl(n), d !== 0 && (o = d, r = Ys(n, d))), r === 1)) throw l = Ps, al(n, 0), ci(n, o), ia(n, Je()), l;
        switch (n.finishedWork = c, n.finishedLanes = o, r) {
          case 0:
          case 1:
            throw Error(T(345));
          case 2:
            Vu(n, aa, Ea);
            break;
          case 3:
            if (ci(n, o), (o & 130023424) === o && (r = Gd + 500 - Je(), 10 < r)) {
              if (ni(n, 0) !== 0) break;
              if (c = n.suspendedLanes, (c & o) !== o) {
                Vn(), n.pingedLanes |= n.suspendedLanes & c;
                break;
              }
              n.timeoutHandle = Dc(Vu.bind(null, n, aa, Ea), r);
              break;
            }
            Vu(n, aa, Ea);
            break;
          case 4:
            if (ci(n, o), (o & 4194240) === o) break;
            for (r = n.eventTimes, c = -1; 0 < o; ) {
              var m = 31 - Or(o);
              d = 1 << m, m = r[m], m > c && (c = m), o &= ~d;
            }
            if (o = c, o = Je() - o, o = (120 > o ? 120 : 480 > o ? 480 : 1080 > o ? 1080 : 1920 > o ? 1920 : 3e3 > o ? 3e3 : 4320 > o ? 4320 : 1960 * Sy(o / 1960)) - o, 10 < o) {
              n.timeoutHandle = Dc(Vu.bind(null, n, aa, Ea), o);
              break;
            }
            Vu(n, aa, Ea);
            break;
          case 5:
            Vu(n, aa, Ea);
            break;
          default:
            throw Error(T(329));
        }
      }
    }
    return ia(n, Je()), n.callbackNode === l ? vf.bind(null, n) : null;
  }
  function Ys(n, r) {
    var l = Bs;
    return n.current.memoizedState.isDehydrated && (al(n, r).flags |= 256), n = hf(n, r), n !== 2 && (r = aa, aa = l, r !== null && Fu(r)), n;
  }
  function Fu(n) {
    aa === null ? aa = n : aa.push.apply(aa, n);
  }
  function Ey(n) {
    for (var r = n; ; ) {
      if (r.flags & 16384) {
        var l = r.updateQueue;
        if (l !== null && (l = l.stores, l !== null)) for (var o = 0; o < l.length; o++) {
          var c = l[o], d = c.getSnapshot;
          c = c.value;
          try {
            if (!ii(d(), c)) return !1;
          } catch {
            return !1;
          }
        }
      }
      if (l = r.child, r.subtreeFlags & 16384 && l !== null) l.return = r, r = l;
      else {
        if (r === n) break;
        for (; r.sibling === null; ) {
          if (r.return === null || r.return === n) return !0;
          r = r.return;
        }
        r.sibling.return = r.return, r = r.sibling;
      }
    }
    return !0;
  }
  function ci(n, r) {
    for (r &= ~df, r &= ~Do, n.suspendedLanes |= r, n.pingedLanes &= ~r, n = n.expirationTimes; 0 < r; ) {
      var l = 31 - Or(r), o = 1 << l;
      n[l] = -1, r &= ~o;
    }
  }
  function qd(n) {
    if (_t & 6) throw Error(T(327));
    Mo();
    var r = ni(n, 0);
    if (!(r & 1)) return ia(n, Je()), null;
    var l = hf(n, r);
    if (n.tag !== 0 && l === 2) {
      var o = bl(n);
      o !== 0 && (r = o, l = Ys(n, o));
    }
    if (l === 1) throw l = Ps, al(n, 0), ci(n, r), ia(n, Je()), l;
    if (l === 6) throw Error(T(345));
    return n.finishedWork = n.current.alternate, n.finishedLanes = r, Vu(n, aa, Ea), ia(n, Je()), null;
  }
  function Kd(n, r) {
    var l = _t;
    _t |= 1;
    try {
      return n(r);
    } finally {
      _t = l, _t === 0 && (Oo = Je() + 500, _o && xi());
    }
  }
  function Hu(n) {
    rl !== null && rl.tag === 0 && !(_t & 6) && Mo();
    var r = _t;
    _t |= 1;
    var l = cr.transition, o = Lt;
    try {
      if (cr.transition = null, Lt = 1, n) return n();
    } finally {
      Lt = o, cr.transition = l, _t = r, !(_t & 6) && xi();
    }
  }
  function Xd() {
    Sa = ko.current, an(ko);
  }
  function al(n, r) {
    n.finishedWork = null, n.finishedLanes = 0;
    var l = n.timeoutHandle;
    if (l !== -1 && (n.timeoutHandle = -1, Ed(l)), Hn !== null) for (l = Hn.return; l !== null; ) {
      var o = l;
      switch (Uc(o), o.tag) {
        case 1:
          o = o.type.childContextTypes, o != null && Co();
          break;
        case 3:
          xu(), an(Wn), an(Cn), Ne();
          break;
        case 5:
          Fc(o);
          break;
        case 4:
          xu();
          break;
        case 13:
          an(Sn);
          break;
        case 19:
          an(Sn);
          break;
        case 10:
          wd(o.type._context);
          break;
        case 22:
        case 23:
          Xd();
      }
      l = l.return;
    }
    if (qn = n, Hn = n = Ql(n.current, null), fr = Sa = r, kn = 0, Ps = null, df = Do = Ui = 0, aa = Bs = null, bu !== null) {
      for (r = 0; r < bu.length; r++) if (l = bu[r], o = l.interleaved, o !== null) {
        l.interleaved = null;
        var c = o.next, d = l.pending;
        if (d !== null) {
          var m = d.next;
          d.next = c, o.next = m;
        }
        l.pending = o;
      }
      bu = null;
    }
    return n;
  }
  function uh(n, r) {
    do {
      var l = Hn;
      try {
        if (bd(), ct.current = Mu, Vc) {
          for (var o = Ut.memoizedState; o !== null; ) {
            var c = o.queue;
            c !== null && (c.pending = null), o = o.next;
          }
          Vc = !1;
        }
        if (qt = 0, er = An = Ut = null, _s = !1, ku = 0, Au.current = null, l === null || l.return === null) {
          kn = 1, Ps = r, Hn = null;
          break;
        }
        e: {
          var d = n, m = l.return, E = l, R = r;
          if (r = fr, E.flags |= 32768, R !== null && typeof R == "object" && typeof R.then == "function") {
            var j = R, W = E, q = W.tag;
            if (!(W.mode & 1) && (q === 0 || q === 11 || q === 15)) {
              var Q = W.alternate;
              Q ? (W.updateQueue = Q.updateQueue, W.memoizedState = Q.memoizedState, W.lanes = Q.lanes) : (W.updateQueue = null, W.memoizedState = null);
            }
            var pe = Gv(m);
            if (pe !== null) {
              pe.flags &= -257, Bl(pe, m, E, d, r), pe.mode & 1 && Hd(d, j, r), r = pe, R = j;
              var Se = r.updateQueue;
              if (Se === null) {
                var _e = /* @__PURE__ */ new Set();
                _e.add(R), r.updateQueue = _e;
              } else Se.add(R);
              break e;
            } else {
              if (!(r & 1)) {
                Hd(d, j, r), Zd();
                break e;
              }
              R = Error(T(426));
            }
          } else if (pn && E.mode & 1) {
            var Dn = Gv(m);
            if (Dn !== null) {
              !(Dn.flags & 65536) && (Dn.flags |= 256), Bl(Dn, m, E, d, r), Ji(Uu(R, E));
              break e;
            }
          }
          d = R = Uu(R, E), kn !== 4 && (kn = 2), Bs === null ? Bs = [d] : Bs.push(d), d = m;
          do {
            switch (d.tag) {
              case 3:
                d.flags |= 65536, r &= -r, d.lanes |= r;
                var D = Wv(d, R, r);
                Bv(d, D);
                break e;
              case 1:
                E = R;
                var w = d.type, M = d.stateNode;
                if (!(d.flags & 128) && (typeof w.getDerivedStateFromError == "function" || M !== null && typeof M.componentDidCatch == "function" && (Il === null || !Il.has(M)))) {
                  d.flags |= 65536, r &= -r, d.lanes |= r;
                  var G = Fd(d, E, r);
                  Bv(d, G);
                  break e;
                }
            }
            d = d.return;
          } while (d !== null);
        }
        fh(l);
      } catch (Ee) {
        r = Ee, Hn === l && l !== null && (Hn = l = l.return);
        continue;
      }
      break;
    } while (!0);
  }
  function oh() {
    var n = $l.current;
    return $l.current = Mu, n === null ? Mu : n;
  }
  function Zd() {
    (kn === 0 || kn === 3 || kn === 2) && (kn = 4), qn === null || !(Ui & 268435455) && !(Do & 268435455) || ci(qn, fr);
  }
  function hf(n, r) {
    var l = _t;
    _t |= 2;
    var o = oh();
    (qn !== n || fr !== r) && (Ea = null, al(n, r));
    do
      try {
        Cy();
        break;
      } catch (c) {
        uh(n, c);
      }
    while (!0);
    if (bd(), _t = l, $l.current = o, Hn !== null) throw Error(T(261));
    return qn = null, fr = 0, kn;
  }
  function Cy() {
    for (; Hn !== null; ) ch(Hn);
  }
  function sh() {
    for (; Hn !== null && !Za(); ) ch(Hn);
  }
  function ch(n) {
    var r = hh(n.alternate, n, Sa);
    n.memoizedProps = n.pendingProps, r === null ? fh(n) : Hn = r, Au.current = null;
  }
  function fh(n) {
    var r = n;
    do {
      var l = r.alternate;
      if (n = r.return, r.flags & 32768) {
        if (l = sf(l, r), l !== null) {
          l.flags &= 32767, Hn = l;
          return;
        }
        if (n !== null) n.flags |= 32768, n.subtreeFlags = 0, n.deletions = null;
        else {
          kn = 6, Hn = null;
          return;
        }
      } else if (l = th(l, r, Sa), l !== null) {
        Hn = l;
        return;
      }
      if (r = r.sibling, r !== null) {
        Hn = r;
        return;
      }
      Hn = r = n;
    } while (r !== null);
    kn === 0 && (kn = 5);
  }
  function Vu(n, r, l) {
    var o = Lt, c = cr.transition;
    try {
      cr.transition = null, Lt = 1, _y(n, r, l, o);
    } finally {
      cr.transition = c, Lt = o;
    }
    return null;
  }
  function _y(n, r, l, o) {
    do
      Mo();
    while (rl !== null);
    if (_t & 6) throw Error(T(327));
    l = n.finishedWork;
    var c = n.finishedLanes;
    if (l === null) return null;
    if (n.finishedWork = null, n.finishedLanes = 0, l === n.current) throw Error(T(177));
    n.callbackNode = null, n.callbackPriority = 0;
    var d = l.lanes | l.childLanes;
    if (Jf(n, d), n === qn && (Hn = qn = null, fr = 0), !(l.subtreeFlags & 2064) && !(l.flags & 2064) || pf || (pf = !0, mh(cu, function() {
      return Mo(), null;
    })), d = (l.flags & 15990) !== 0, l.subtreeFlags & 15990 || d) {
      d = cr.transition, cr.transition = null;
      var m = Lt;
      Lt = 1;
      var E = _t;
      _t |= 4, Au.current = null, rh(n, l), Yd(l, n), vo(Eu), Oa = !!ds, Eu = ds = null, n.current = l, gy(l), Ja(), _t = E, Lt = m, cr.transition = d;
    } else n.current = l;
    if (pf && (pf = !1, rl = n, $s = c), d = n.pendingLanes, d === 0 && (Il = null), Zo(l.stateNode), ia(n, Je()), r !== null) for (o = n.onRecoverableError, l = 0; l < r.length; l++) c = r[l], o(c.value, { componentStack: c.stack, digest: c.digest });
    if (No) throw No = !1, n = ju, ju = null, n;
    return $s & 1 && n.tag !== 0 && Mo(), d = n.pendingLanes, d & 1 ? n === Lo ? Yl++ : (Yl = 0, Lo = n) : Yl = 0, xi(), null;
  }
  function Mo() {
    if (rl !== null) {
      var n = io($s), r = cr.transition, l = Lt;
      try {
        if (cr.transition = null, Lt = 16 > n ? 16 : n, rl === null) var o = !1;
        else {
          if (n = rl, rl = null, $s = 0, _t & 6) throw Error(T(331));
          var c = _t;
          for (_t |= 4, ye = n.current; ye !== null; ) {
            var d = ye, m = d.child;
            if (ye.flags & 16) {
              var E = d.deletions;
              if (E !== null) {
                for (var R = 0; R < E.length; R++) {
                  var j = E[R];
                  for (ye = j; ye !== null; ) {
                    var W = ye;
                    switch (W.tag) {
                      case 0:
                      case 11:
                      case 15:
                        js(8, W, d);
                    }
                    var q = W.child;
                    if (q !== null) q.return = W, ye = q;
                    else for (; ye !== null; ) {
                      W = ye;
                      var Q = W.sibling, pe = W.return;
                      if (ff(W), W === j) {
                        ye = null;
                        break;
                      }
                      if (Q !== null) {
                        Q.return = pe, ye = Q;
                        break;
                      }
                      ye = pe;
                    }
                  }
                }
                var Se = d.alternate;
                if (Se !== null) {
                  var _e = Se.child;
                  if (_e !== null) {
                    Se.child = null;
                    do {
                      var Dn = _e.sibling;
                      _e.sibling = null, _e = Dn;
                    } while (_e !== null);
                  }
                }
                ye = d;
              }
            }
            if (d.subtreeFlags & 2064 && m !== null) m.return = d, ye = m;
            else e: for (; ye !== null; ) {
              if (d = ye, d.flags & 2048) switch (d.tag) {
                case 0:
                case 11:
                case 15:
                  js(9, d, d.return);
              }
              var D = d.sibling;
              if (D !== null) {
                D.return = d.return, ye = D;
                break e;
              }
              ye = d.return;
            }
          }
          var w = n.current;
          for (ye = w; ye !== null; ) {
            m = ye;
            var M = m.child;
            if (m.subtreeFlags & 2064 && M !== null) M.return = m, ye = M;
            else e: for (m = w; ye !== null; ) {
              if (E = ye, E.flags & 2048) try {
                switch (E.tag) {
                  case 0:
                  case 11:
                  case 15:
                    Fs(9, E);
                }
              } catch (Ee) {
                vn(E, E.return, Ee);
              }
              if (E === m) {
                ye = null;
                break e;
              }
              var G = E.sibling;
              if (G !== null) {
                G.return = E.return, ye = G;
                break e;
              }
              ye = E.return;
            }
          }
          if (_t = c, xi(), Gr && typeof Gr.onPostCommitFiberRoot == "function") try {
            Gr.onPostCommitFiberRoot(Rl, n);
          } catch {
          }
          o = !0;
        }
        return o;
      } finally {
        Lt = l, cr.transition = r;
      }
    }
    return !1;
  }
  function dh(n, r, l) {
    r = Uu(l, r), r = Wv(n, r, 1), n = Hl(n, r, 1), r = Vn(), n !== null && (Ii(n, 1, r), ia(n, r));
  }
  function vn(n, r, l) {
    if (n.tag === 3) dh(n, n, l);
    else for (; r !== null; ) {
      if (r.tag === 3) {
        dh(r, n, l);
        break;
      } else if (r.tag === 1) {
        var o = r.stateNode;
        if (typeof r.type.getDerivedStateFromError == "function" || typeof o.componentDidCatch == "function" && (Il === null || !Il.has(o))) {
          n = Uu(l, n), n = Fd(r, n, 1), r = Hl(r, n, 1), n = Vn(), r !== null && (Ii(r, 1, n), ia(r, n));
          break;
        }
      }
      r = r.return;
    }
  }
  function Ry(n, r, l) {
    var o = n.pingCache;
    o !== null && o.delete(r), r = Vn(), n.pingedLanes |= n.suspendedLanes & l, qn === n && (fr & l) === l && (kn === 4 || kn === 3 && (fr & 130023424) === fr && 500 > Je() - Gd ? al(n, 0) : df |= l), ia(n, r);
  }
  function ph(n, r) {
    r === 0 && (n.mode & 1 ? (r = va, va <<= 1, !(va & 130023424) && (va = 4194304)) : r = 1);
    var l = Vn();
    n = ya(n, r), n !== null && (Ii(n, r, l), ia(n, l));
  }
  function Ty(n) {
    var r = n.memoizedState, l = 0;
    r !== null && (l = r.retryLane), ph(n, l);
  }
  function vh(n, r) {
    var l = 0;
    switch (n.tag) {
      case 13:
        var o = n.stateNode, c = n.memoizedState;
        c !== null && (l = c.retryLane);
        break;
      case 19:
        o = n.stateNode;
        break;
      default:
        throw Error(T(314));
    }
    o !== null && o.delete(r), ph(n, l);
  }
  var hh;
  hh = function(n, r, l) {
    if (n !== null) if (n.memoizedProps !== r.pendingProps || Wn.current) jn = !0;
    else {
      if (!(n.lanes & l) && !(r.flags & 128)) return jn = !1, Us(n, r, l);
      jn = !!(n.flags & 131072);
    }
    else jn = !1, pn && r.flags & 1048576 && Fv(r, Zi, r.index);
    switch (r.lanes = 0, r.tag) {
      case 2:
        var o = r.type;
        ja(n, r), n = r.pendingProps;
        var c = Xr(r, Cn.current);
        gn(r, l), c = Vl(null, r, o, n, c, l);
        var d = ui();
        return r.flags |= 1, typeof c == "object" && c !== null && typeof c.render == "function" && c.$$typeof === void 0 ? (r.tag = 1, r.memoizedState = null, r.updateQueue = null, Un(o) ? (d = !0, Jn(r)) : d = !1, r.memoizedState = c.state !== null && c.state !== void 0 ? c.state : null, Od(r), c.updater = rf, r.stateNode = c, c._reactInternals = r, Ds(r, o, n, l), r = Ls(null, r, o, !0, d, l)) : (r.tag = 0, pn && d && Mc(r), sr(null, r, c, l), r = r.child), r;
      case 16:
        o = r.elementType;
        e: {
          switch (ja(n, r), n = r.pendingProps, c = o._init, o = c(o._payload), r.type = o, c = r.tag = wy(o), n = oi(o, n), c) {
            case 0:
              r = qv(null, r, o, n, l);
              break e;
            case 1:
              r = Kv(null, r, o, n, l);
              break e;
            case 11:
              r = na(null, r, o, n, l);
              break e;
            case 14:
              r = zu(null, r, o, oi(o.type, n), l);
              break e;
          }
          throw Error(T(
            306,
            o,
            ""
          ));
        }
        return r;
      case 0:
        return o = r.type, c = r.pendingProps, c = r.elementType === o ? c : oi(o, c), qv(n, r, o, c, l);
      case 1:
        return o = r.type, c = r.pendingProps, c = r.elementType === o ? c : oi(o, c), Kv(n, r, o, c, l);
      case 3:
        e: {
          if (wo(r), n === null) throw Error(T(387));
          o = r.pendingProps, d = r.memoizedState, c = d.element, Pv(n, r), ys(r, o, null, l);
          var m = r.memoizedState;
          if (o = m.element, d.isDehydrated) if (d = { element: o, isDehydrated: !1, cache: m.cache, pendingSuspenseBoundaries: m.pendingSuspenseBoundaries, transitions: m.transitions }, r.updateQueue.baseState = d, r.memoizedState = d, r.flags & 256) {
            c = Uu(Error(T(423)), r), r = Xv(n, r, o, l, c);
            break e;
          } else if (o !== c) {
            c = Uu(Error(T(424)), r), r = Xv(n, r, o, l, c);
            break e;
          } else for (Jr = Ti(r.stateNode.containerInfo.firstChild), Zr = r, pn = !0, za = null, l = se(r, null, o, l), r.child = l; l; ) l.flags = l.flags & -3 | 4096, l = l.sibling;
          else {
            if (Fl(), o === c) {
              r = Fa(n, r, l);
              break e;
            }
            sr(n, r, o, l);
          }
          r = r.child;
        }
        return r;
      case 5:
        return $v(r), n === null && Rd(r), o = r.type, c = r.pendingProps, d = n !== null ? n.memoizedProps : null, m = c.children, kc(o, c) ? m = null : d !== null && kc(o, d) && (r.flags |= 32), Vd(n, r), sr(n, r, m, l), r.child;
      case 6:
        return n === null && Rd(r), null;
      case 13:
        return of(n, r, l);
      case 4:
        return Ld(r, r.stateNode.containerInfo), o = r.pendingProps, n === null ? r.child = bn(r, null, o, l) : sr(n, r, o, l), r.child;
      case 11:
        return o = r.type, c = r.pendingProps, c = r.elementType === o ? c : oi(o, c), na(n, r, o, c, l);
      case 7:
        return sr(n, r, r.pendingProps, l), r.child;
      case 8:
        return sr(n, r, r.pendingProps.children, l), r.child;
      case 12:
        return sr(n, r, r.pendingProps.children, l), r.child;
      case 10:
        e: {
          if (o = r.type._context, c = r.pendingProps, d = r.memoizedProps, m = c.value, xe(ma, o._currentValue), o._currentValue = m, d !== null) if (ii(d.value, m)) {
            if (d.children === c.children && !Wn.current) {
              r = Fa(n, r, l);
              break e;
            }
          } else for (d = r.child, d !== null && (d.return = r); d !== null; ) {
            var E = d.dependencies;
            if (E !== null) {
              m = d.child;
              for (var R = E.firstContext; R !== null; ) {
                if (R.context === o) {
                  if (d.tag === 1) {
                    R = el(-1, l & -l), R.tag = 2;
                    var j = d.updateQueue;
                    if (j !== null) {
                      j = j.shared;
                      var W = j.pending;
                      W === null ? R.next = R : (R.next = W.next, W.next = R), j.pending = R;
                    }
                  }
                  d.lanes |= l, R = d.alternate, R !== null && (R.lanes |= l), xd(
                    d.return,
                    l,
                    r
                  ), E.lanes |= l;
                  break;
                }
                R = R.next;
              }
            } else if (d.tag === 10) m = d.type === r.type ? null : d.child;
            else if (d.tag === 18) {
              if (m = d.return, m === null) throw Error(T(341));
              m.lanes |= l, E = m.alternate, E !== null && (E.lanes |= l), xd(m, l, r), m = d.sibling;
            } else m = d.child;
            if (m !== null) m.return = d;
            else for (m = d; m !== null; ) {
              if (m === r) {
                m = null;
                break;
              }
              if (d = m.sibling, d !== null) {
                d.return = m.return, m = d;
                break;
              }
              m = m.return;
            }
            d = m;
          }
          sr(n, r, c.children, l), r = r.child;
        }
        return r;
      case 9:
        return c = r.type, o = r.pendingProps.children, gn(r, l), c = Aa(c), o = o(c), r.flags |= 1, sr(n, r, o, l), r.child;
      case 14:
        return o = r.type, c = oi(o, r.pendingProps), c = oi(o.type, c), zu(n, r, o, c, l);
      case 15:
        return et(n, r, r.type, r.pendingProps, l);
      case 17:
        return o = r.type, c = r.pendingProps, c = r.elementType === o ? c : oi(o, c), ja(n, r), r.tag = 1, Un(o) ? (n = !0, Jn(r)) : n = !1, gn(r, l), af(r, o, c), Ds(r, o, c, l), Ls(null, r, o, !0, n, l);
      case 19:
        return Ni(n, r, l);
      case 22:
        return Ns(n, r, l);
    }
    throw Error(T(156, r.tag));
  };
  function mh(n, r) {
    return sn(n, r);
  }
  function by(n, r, l, o) {
    this.tag = n, this.key = l, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = r, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = o, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
  }
  function Va(n, r, l, o) {
    return new by(n, r, l, o);
  }
  function Jd(n) {
    return n = n.prototype, !(!n || !n.isReactComponent);
  }
  function wy(n) {
    if (typeof n == "function") return Jd(n) ? 1 : 0;
    if (n != null) {
      if (n = n.$$typeof, n === kt) return 11;
      if (n === Dt) return 14;
    }
    return 2;
  }
  function Ql(n, r) {
    var l = n.alternate;
    return l === null ? (l = Va(n.tag, r, n.key, n.mode), l.elementType = n.elementType, l.type = n.type, l.stateNode = n.stateNode, l.alternate = n, n.alternate = l) : (l.pendingProps = r, l.type = n.type, l.flags = 0, l.subtreeFlags = 0, l.deletions = null), l.flags = n.flags & 14680064, l.childLanes = n.childLanes, l.lanes = n.lanes, l.child = n.child, l.memoizedProps = n.memoizedProps, l.memoizedState = n.memoizedState, l.updateQueue = n.updateQueue, r = n.dependencies, l.dependencies = r === null ? null : { lanes: r.lanes, firstContext: r.firstContext }, l.sibling = n.sibling, l.index = n.index, l.ref = n.ref, l;
  }
  function Qs(n, r, l, o, c, d) {
    var m = 2;
    if (o = n, typeof n == "function") Jd(n) && (m = 1);
    else if (typeof n == "string") m = 5;
    else e: switch (n) {
      case Be:
        return il(l.children, c, d, r);
      case ln:
        m = 8, c |= 8;
        break;
      case Vt:
        return n = Va(12, l, r, c | 2), n.elementType = Vt, n.lanes = d, n;
      case Le:
        return n = Va(13, l, r, c), n.elementType = Le, n.lanes = d, n;
      case Ft:
        return n = Va(19, l, r, c), n.elementType = Ft, n.lanes = d, n;
      case Re:
        return Wl(l, c, d, r);
      default:
        if (typeof n == "object" && n !== null) switch (n.$$typeof) {
          case Jt:
            m = 10;
            break e;
          case un:
            m = 9;
            break e;
          case kt:
            m = 11;
            break e;
          case Dt:
            m = 14;
            break e;
          case Nt:
            m = 16, o = null;
            break e;
        }
        throw Error(T(130, n == null ? n : typeof n, ""));
    }
    return r = Va(m, l, r, c), r.elementType = n, r.type = o, r.lanes = d, r;
  }
  function il(n, r, l, o) {
    return n = Va(7, n, o, r), n.lanes = l, n;
  }
  function Wl(n, r, l, o) {
    return n = Va(22, n, o, r), n.elementType = Re, n.lanes = l, n.stateNode = { isHidden: !1 }, n;
  }
  function ep(n, r, l) {
    return n = Va(6, n, null, r), n.lanes = l, n;
  }
  function mf(n, r, l) {
    return r = Va(4, n.children !== null ? n.children : [], n.key, r), r.lanes = l, r.stateNode = { containerInfo: n.containerInfo, pendingChildren: null, implementation: n.implementation }, r;
  }
  function yh(n, r, l, o, c) {
    this.tag = r, this.containerInfo = n, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = ao(0), this.expirationTimes = ao(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = ao(0), this.identifierPrefix = o, this.onRecoverableError = c, this.mutableSourceEagerHydrationData = null;
  }
  function yf(n, r, l, o, c, d, m, E, R) {
    return n = new yh(n, r, l, E, R), r === 1 ? (r = 1, d === !0 && (r |= 8)) : r = 0, d = Va(3, null, null, r), n.current = d, d.stateNode = n, d.memoizedState = { element: o, isDehydrated: l, cache: null, transitions: null, pendingSuspenseBoundaries: null }, Od(d), n;
  }
  function xy(n, r, l) {
    var o = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
    return { $$typeof: dt, key: o == null ? null : "" + o, children: n, containerInfo: r, implementation: l };
  }
  function tp(n) {
    if (!n) return Rr;
    n = n._reactInternals;
    e: {
      if (Ze(n) !== n || n.tag !== 1) throw Error(T(170));
      var r = n;
      do {
        switch (r.tag) {
          case 3:
            r = r.stateNode.context;
            break e;
          case 1:
            if (Un(r.type)) {
              r = r.stateNode.__reactInternalMemoizedMergedChildContext;
              break e;
            }
        }
        r = r.return;
      } while (r !== null);
      throw Error(T(171));
    }
    if (n.tag === 1) {
      var l = n.type;
      if (Un(l)) return hs(n, l, r);
    }
    return r;
  }
  function gh(n, r, l, o, c, d, m, E, R) {
    return n = yf(l, o, !0, n, c, d, m, E, R), n.context = tp(null), l = n.current, o = Vn(), c = zi(l), d = el(o, c), d.callback = r ?? null, Hl(l, d, c), n.current.lanes = c, Ii(n, c, o), ia(n, o), n;
  }
  function gf(n, r, l, o) {
    var c = r.current, d = Vn(), m = zi(c);
    return l = tp(l), r.context === null ? r.context = l : r.pendingContext = l, r = el(d, m), r.payload = { element: n }, o = o === void 0 ? null : o, o !== null && (r.callback = o), n = Hl(c, r, m), n !== null && (Ar(n, c, m, d), jc(n, c, m)), m;
  }
  function Sf(n) {
    if (n = n.current, !n.child) return null;
    switch (n.child.tag) {
      case 5:
        return n.child.stateNode;
      default:
        return n.child.stateNode;
    }
  }
  function np(n, r) {
    if (n = n.memoizedState, n !== null && n.dehydrated !== null) {
      var l = n.retryLane;
      n.retryLane = l !== 0 && l < r ? l : r;
    }
  }
  function Ef(n, r) {
    np(n, r), (n = n.alternate) && np(n, r);
  }
  function Sh() {
    return null;
  }
  var Pu = typeof reportError == "function" ? reportError : function(n) {
    console.error(n);
  };
  function rp(n) {
    this._internalRoot = n;
  }
  Cf.prototype.render = rp.prototype.render = function(n) {
    var r = this._internalRoot;
    if (r === null) throw Error(T(409));
    gf(n, r, null, null);
  }, Cf.prototype.unmount = rp.prototype.unmount = function() {
    var n = this._internalRoot;
    if (n !== null) {
      this._internalRoot = null;
      var r = n.containerInfo;
      Hu(function() {
        gf(null, n, null, null);
      }), r[Ki] = null;
    }
  };
  function Cf(n) {
    this._internalRoot = n;
  }
  Cf.prototype.unstable_scheduleHydration = function(n) {
    if (n) {
      var r = Qe();
      n = { blockedOn: null, target: n, priority: r };
      for (var l = 0; l < Qn.length && r !== 0 && r < Qn[l].priority; l++) ;
      Qn.splice(l, 0, n), l === 0 && ts(n);
    }
  };
  function ap(n) {
    return !(!n || n.nodeType !== 1 && n.nodeType !== 9 && n.nodeType !== 11);
  }
  function _f(n) {
    return !(!n || n.nodeType !== 1 && n.nodeType !== 9 && n.nodeType !== 11 && (n.nodeType !== 8 || n.nodeValue !== " react-mount-point-unstable "));
  }
  function Eh() {
  }
  function ky(n, r, l, o, c) {
    if (c) {
      if (typeof o == "function") {
        var d = o;
        o = function() {
          var j = Sf(m);
          d.call(j);
        };
      }
      var m = gh(r, o, n, 0, null, !1, !1, "", Eh);
      return n._reactRootContainer = m, n[Ki] = m.current, mo(n.nodeType === 8 ? n.parentNode : n), Hu(), m;
    }
    for (; c = n.lastChild; ) n.removeChild(c);
    if (typeof o == "function") {
      var E = o;
      o = function() {
        var j = Sf(R);
        E.call(j);
      };
    }
    var R = yf(n, 0, !1, null, null, !1, !1, "", Eh);
    return n._reactRootContainer = R, n[Ki] = R.current, mo(n.nodeType === 8 ? n.parentNode : n), Hu(function() {
      gf(r, R, l, o);
    }), R;
  }
  function Ws(n, r, l, o, c) {
    var d = l._reactRootContainer;
    if (d) {
      var m = d;
      if (typeof c == "function") {
        var E = c;
        c = function() {
          var R = Sf(m);
          E.call(R);
        };
      }
      gf(r, m, n, c);
    } else m = ky(l, r, n, c, o);
    return Sf(m);
  }
  wt = function(n) {
    switch (n.tag) {
      case 3:
        var r = n.stateNode;
        if (r.current.memoizedState.isDehydrated) {
          var l = ti(r.pendingLanes);
          l !== 0 && (Yi(r, l | 1), ia(r, Je()), !(_t & 6) && (Oo = Je() + 500, xi()));
        }
        break;
      case 13:
        Hu(function() {
          var o = ya(n, 1);
          if (o !== null) {
            var c = Vn();
            Ar(o, n, 1, c);
          }
        }), Ef(n, 1);
    }
  }, Jo = function(n) {
    if (n.tag === 13) {
      var r = ya(n, 134217728);
      if (r !== null) {
        var l = Vn();
        Ar(r, n, 134217728, l);
      }
      Ef(n, 134217728);
    }
  }, Si = function(n) {
    if (n.tag === 13) {
      var r = zi(n), l = ya(n, r);
      if (l !== null) {
        var o = Vn();
        Ar(l, n, r, o);
      }
      Ef(n, r);
    }
  }, Qe = function() {
    return Lt;
  }, lo = function(n, r) {
    var l = Lt;
    try {
      return Lt = n, r();
    } finally {
      Lt = l;
    }
  }, Yt = function(n, r, l) {
    switch (r) {
      case "input":
        if (Wr(n, l), r = l.name, l.type === "radio" && r != null) {
          for (l = n; l.parentNode; ) l = l.parentNode;
          for (l = l.querySelectorAll("input[name=" + JSON.stringify("" + r) + '][type="radio"]'), r = 0; r < l.length; r++) {
            var o = l[r];
            if (o !== n && o.form === n.form) {
              var c = yn(o);
              if (!c) throw Error(T(90));
              xr(o), Wr(o, c);
            }
          }
        }
        break;
      case "textarea":
        qa(n, l);
        break;
      case "select":
        r = l.value, r != null && Rn(n, !!l.multiple, r, !1);
    }
  }, uu = Kd, El = Hu;
  var Dy = { usingClientEntryPoint: !1, Events: [Oe, li, yn, $i, lu, Kd] }, Gs = { findFiberByHostInstance: Cu, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, Ch = { bundleType: Gs.bundleType, version: Gs.version, rendererPackageName: Gs.rendererPackageName, rendererConfig: Gs.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: yt.ReactCurrentDispatcher, findHostInstanceByFiber: function(n) {
    return n = Tn(n), n === null ? null : n.stateNode;
  }, findFiberByHostInstance: Gs.findFiberByHostInstance || Sh, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
    var Gl = __REACT_DEVTOOLS_GLOBAL_HOOK__;
    if (!Gl.isDisabled && Gl.supportsFiber) try {
      Rl = Gl.inject(Ch), Gr = Gl;
    } catch {
    }
  }
  return Qa.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Dy, Qa.createPortal = function(n, r) {
    var l = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
    if (!ap(r)) throw Error(T(200));
    return xy(n, r, null, l);
  }, Qa.createRoot = function(n, r) {
    if (!ap(n)) throw Error(T(299));
    var l = !1, o = "", c = Pu;
    return r != null && (r.unstable_strictMode === !0 && (l = !0), r.identifierPrefix !== void 0 && (o = r.identifierPrefix), r.onRecoverableError !== void 0 && (c = r.onRecoverableError)), r = yf(n, 1, !1, null, null, l, !1, o, c), n[Ki] = r.current, mo(n.nodeType === 8 ? n.parentNode : n), new rp(r);
  }, Qa.findDOMNode = function(n) {
    if (n == null) return null;
    if (n.nodeType === 1) return n;
    var r = n._reactInternals;
    if (r === void 0)
      throw typeof n.render == "function" ? Error(T(188)) : (n = Object.keys(n).join(","), Error(T(268, n)));
    return n = Tn(r), n = n === null ? null : n.stateNode, n;
  }, Qa.flushSync = function(n) {
    return Hu(n);
  }, Qa.hydrate = function(n, r, l) {
    if (!_f(r)) throw Error(T(200));
    return Ws(null, n, r, !0, l);
  }, Qa.hydrateRoot = function(n, r, l) {
    if (!ap(n)) throw Error(T(405));
    var o = l != null && l.hydratedSources || null, c = !1, d = "", m = Pu;
    if (l != null && (l.unstable_strictMode === !0 && (c = !0), l.identifierPrefix !== void 0 && (d = l.identifierPrefix), l.onRecoverableError !== void 0 && (m = l.onRecoverableError)), r = gh(r, null, n, 1, l ?? null, c, !1, d, m), n[Ki] = r.current, mo(n), o) for (n = 0; n < o.length; n++) l = o[n], c = l._getVersion, c = c(l._source), r.mutableSourceEagerHydrationData == null ? r.mutableSourceEagerHydrationData = [l, c] : r.mutableSourceEagerHydrationData.push(
      l,
      c
    );
    return new Cf(r);
  }, Qa.render = function(n, r, l) {
    if (!_f(r)) throw Error(T(200));
    return Ws(null, n, r, !1, l);
  }, Qa.unmountComponentAtNode = function(n) {
    if (!_f(n)) throw Error(T(40));
    return n._reactRootContainer ? (Hu(function() {
      Ws(null, null, n, !1, function() {
        n._reactRootContainer = null, n[Ki] = null;
      });
    }), !0) : !1;
  }, Qa.unstable_batchedUpdates = Kd, Qa.unstable_renderSubtreeIntoContainer = function(n, r, l, o) {
    if (!_f(l)) throw Error(T(200));
    if (n == null || n._reactInternals === void 0) throw Error(T(38));
    return Ws(n, r, l, !1, o);
  }, Qa.version = "18.3.1-next-f1338f8080-20240426", Qa;
}
var Wa = {};
/**
 * @license React
 * react-dom.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var vR;
function vk() {
  return vR || (vR = 1, process.env.NODE_ENV !== "production" && function() {
    typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(new Error());
    var O = Qr, A = SR(), T = O.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, oe = !1;
    function ke(e) {
      oe = e;
    }
    function He(e) {
      if (!oe) {
        for (var t = arguments.length, a = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
          a[i - 1] = arguments[i];
        ft("warn", e, a);
      }
    }
    function S(e) {
      if (!oe) {
        for (var t = arguments.length, a = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
          a[i - 1] = arguments[i];
        ft("error", e, a);
      }
    }
    function ft(e, t, a) {
      {
        var i = T.ReactDebugCurrentFrame, u = i.getStackAddendum();
        u !== "" && (t += "%s", a = a.concat([u]));
        var s = a.map(function(f) {
          return String(f);
        });
        s.unshift("Warning: " + t), Function.prototype.apply.call(console[e], console, s);
      }
    }
    var ee = 0, ne = 1, Ve = 2, te = 3, me = 4, fe = 5, qe = 6, Et = 7, mt = 8, dn = 9, ht = 10, Ke = 11, yt = 12, De = 13, dt = 14, Be = 15, ln = 16, Vt = 17, Jt = 18, un = 19, kt = 21, Le = 22, Ft = 23, Dt = 24, Nt = 25, Re = !0, J = !1, Te = !1, ie = !1, k = !1, B = !0, $e = !0, Fe = !0, ut = !0, rt = /* @__PURE__ */ new Set(), tt = {}, at = {};
    function ot(e, t) {
      $t(e, t), $t(e + "Capture", t);
    }
    function $t(e, t) {
      tt[e] && S("EventRegistry: More than one plugin attempted to publish the same registration name, `%s`.", e), tt[e] = t;
      {
        var a = e.toLowerCase();
        at[a] = e, e === "onDoubleClick" && (at.ondblclick = e);
      }
      for (var i = 0; i < t.length; i++)
        rt.add(t[i]);
    }
    var Nn = typeof window < "u" && typeof window.document < "u" && typeof window.document.createElement < "u", xr = Object.prototype.hasOwnProperty;
    function _n(e) {
      {
        var t = typeof Symbol == "function" && Symbol.toStringTag, a = t && e[Symbol.toStringTag] || e.constructor.name || "Object";
        return a;
      }
    }
    function ar(e) {
      try {
        return $n(e), !1;
      } catch {
        return !0;
      }
    }
    function $n(e) {
      return "" + e;
    }
    function In(e, t) {
      if (ar(e))
        return S("The provided `%s` attribute is an unsupported type %s. This value must be coerced to a string before before using it here.", t, _n(e)), $n(e);
    }
    function Wr(e) {
      if (ar(e))
        return S("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", _n(e)), $n(e);
    }
    function vi(e, t) {
      if (ar(e))
        return S("The provided `%s` prop is an unsupported type %s. This value must be coerced to a string before before using it here.", t, _n(e)), $n(e);
    }
    function fa(e, t) {
      if (ar(e))
        return S("The provided `%s` CSS property is an unsupported type %s. This value must be coerced to a string before before using it here.", t, _n(e)), $n(e);
    }
    function Xn(e) {
      if (ar(e))
        return S("The provided HTML markup uses a value of unsupported type %s. This value must be coerced to a string before before using it here.", _n(e)), $n(e);
    }
    function Rn(e) {
      if (ar(e))
        return S("Form field values (value, checked, defaultValue, or defaultChecked props) must be strings, not %s. This value must be coerced to a string before before using it here.", _n(e)), $n(e);
    }
    var Yn = 0, Er = 1, qa = 2, Ln = 3, Cr = 4, da = 5, Ka = 6, hi = ":A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD", re = hi + "\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040", be = new RegExp("^[" + hi + "][" + re + "]*$"), it = {}, Ht = {};
    function en(e) {
      return xr.call(Ht, e) ? !0 : xr.call(it, e) ? !1 : be.test(e) ? (Ht[e] = !0, !0) : (it[e] = !0, S("Invalid attribute name: `%s`", e), !1);
    }
    function hn(e, t, a) {
      return t !== null ? t.type === Yn : a ? !1 : e.length > 2 && (e[0] === "o" || e[0] === "O") && (e[1] === "n" || e[1] === "N");
    }
    function on(e, t, a, i) {
      if (a !== null && a.type === Yn)
        return !1;
      switch (typeof t) {
        case "function":
        case "symbol":
          return !0;
        case "boolean": {
          if (i)
            return !1;
          if (a !== null)
            return !a.acceptsBooleans;
          var u = e.toLowerCase().slice(0, 5);
          return u !== "data-" && u !== "aria-";
        }
        default:
          return !1;
      }
    }
    function Zn(e, t, a, i) {
      if (t === null || typeof t > "u" || on(e, t, a, i))
        return !0;
      if (i)
        return !1;
      if (a !== null)
        switch (a.type) {
          case Ln:
            return !t;
          case Cr:
            return t === !1;
          case da:
            return isNaN(t);
          case Ka:
            return isNaN(t) || t < 1;
        }
      return !1;
    }
    function tn(e) {
      return Yt.hasOwnProperty(e) ? Yt[e] : null;
    }
    function It(e, t, a, i, u, s, f) {
      this.acceptsBooleans = t === qa || t === Ln || t === Cr, this.attributeName = i, this.attributeNamespace = u, this.mustUseProperty = a, this.propertyName = e, this.type = t, this.sanitizeURL = s, this.removeEmptyString = f;
    }
    var Yt = {}, pa = [
      "children",
      "dangerouslySetInnerHTML",
      // TODO: This prevents the assignment of defaultValue to regular
      // elements (not just inputs). Now that ReactDOMInput assigns to the
      // defaultValue property -- do we need this?
      "defaultValue",
      "defaultChecked",
      "innerHTML",
      "suppressContentEditableWarning",
      "suppressHydrationWarning",
      "style"
    ];
    pa.forEach(function(e) {
      Yt[e] = new It(
        e,
        Yn,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
      var t = e[0], a = e[1];
      Yt[t] = new It(
        t,
        Er,
        !1,
        // mustUseProperty
        a,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
      Yt[e] = new It(
        e,
        qa,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
      Yt[e] = new It(
        e,
        qa,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "allowFullScreen",
      "async",
      // Note: there is a special case that prevents it from being written to the DOM
      // on the client side because the browsers are inconsistent. Instead we call focus().
      "autoFocus",
      "autoPlay",
      "controls",
      "default",
      "defer",
      "disabled",
      "disablePictureInPicture",
      "disableRemotePlayback",
      "formNoValidate",
      "hidden",
      "loop",
      "noModule",
      "noValidate",
      "open",
      "playsInline",
      "readOnly",
      "required",
      "reversed",
      "scoped",
      "seamless",
      // Microdata
      "itemScope"
    ].forEach(function(e) {
      Yt[e] = new It(
        e,
        Ln,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "checked",
      // Note: `option.selected` is not updated if `select.multiple` is
      // disabled with `removeAttribute`. We have special logic for handling this.
      "multiple",
      "muted",
      "selected"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      Yt[e] = new It(
        e,
        Ln,
        !0,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "capture",
      "download"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      Yt[e] = new It(
        e,
        Cr,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "cols",
      "rows",
      "size",
      "span"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      Yt[e] = new It(
        e,
        Ka,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), ["rowSpan", "start"].forEach(function(e) {
      Yt[e] = new It(
        e,
        da,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    });
    var _r = /[\-\:]([a-z])/g, xa = function(e) {
      return e[1].toUpperCase();
    };
    [
      "accent-height",
      "alignment-baseline",
      "arabic-form",
      "baseline-shift",
      "cap-height",
      "clip-path",
      "clip-rule",
      "color-interpolation",
      "color-interpolation-filters",
      "color-profile",
      "color-rendering",
      "dominant-baseline",
      "enable-background",
      "fill-opacity",
      "fill-rule",
      "flood-color",
      "flood-opacity",
      "font-family",
      "font-size",
      "font-size-adjust",
      "font-stretch",
      "font-style",
      "font-variant",
      "font-weight",
      "glyph-name",
      "glyph-orientation-horizontal",
      "glyph-orientation-vertical",
      "horiz-adv-x",
      "horiz-origin-x",
      "image-rendering",
      "letter-spacing",
      "lighting-color",
      "marker-end",
      "marker-mid",
      "marker-start",
      "overline-position",
      "overline-thickness",
      "paint-order",
      "panose-1",
      "pointer-events",
      "rendering-intent",
      "shape-rendering",
      "stop-color",
      "stop-opacity",
      "strikethrough-position",
      "strikethrough-thickness",
      "stroke-dasharray",
      "stroke-dashoffset",
      "stroke-linecap",
      "stroke-linejoin",
      "stroke-miterlimit",
      "stroke-opacity",
      "stroke-width",
      "text-anchor",
      "text-decoration",
      "text-rendering",
      "underline-position",
      "underline-thickness",
      "unicode-bidi",
      "unicode-range",
      "units-per-em",
      "v-alphabetic",
      "v-hanging",
      "v-ideographic",
      "v-mathematical",
      "vector-effect",
      "vert-adv-y",
      "vert-origin-x",
      "vert-origin-y",
      "word-spacing",
      "writing-mode",
      "xmlns:xlink",
      "x-height"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      var t = e.replace(_r, xa);
      Yt[t] = new It(
        t,
        Er,
        !1,
        // mustUseProperty
        e,
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "xlink:actuate",
      "xlink:arcrole",
      "xlink:role",
      "xlink:show",
      "xlink:title",
      "xlink:type"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      var t = e.replace(_r, xa);
      Yt[t] = new It(
        t,
        Er,
        !1,
        // mustUseProperty
        e,
        "http://www.w3.org/1999/xlink",
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "xml:base",
      "xml:lang",
      "xml:space"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      var t = e.replace(_r, xa);
      Yt[t] = new It(
        t,
        Er,
        !1,
        // mustUseProperty
        e,
        "http://www.w3.org/XML/1998/namespace",
        !1,
        // sanitizeURL
        !1
      );
    }), ["tabIndex", "crossOrigin"].forEach(function(e) {
      Yt[e] = new It(
        e,
        Er,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    });
    var $i = "xlinkHref";
    Yt[$i] = new It(
      "xlinkHref",
      Er,
      !1,
      // mustUseProperty
      "xlink:href",
      "http://www.w3.org/1999/xlink",
      !0,
      // sanitizeURL
      !1
    ), ["src", "href", "action", "formAction"].forEach(function(e) {
      Yt[e] = new It(
        e,
        Er,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !0,
        // sanitizeURL
        !0
      );
    });
    var lu = /^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*\:/i, uu = !1;
    function El(e) {
      !uu && lu.test(e) && (uu = !0, S("A future version of React will block javascript: URLs as a security precaution. Use event handlers instead if you can. If you need to generate unsafe HTML try using dangerouslySetInnerHTML instead. React was passed %s.", JSON.stringify(e)));
    }
    function Cl(e, t, a, i) {
      if (i.mustUseProperty) {
        var u = i.propertyName;
        return e[u];
      } else {
        In(a, t), i.sanitizeURL && El("" + a);
        var s = i.attributeName, f = null;
        if (i.type === Cr) {
          if (e.hasAttribute(s)) {
            var p = e.getAttribute(s);
            return p === "" ? !0 : Zn(t, a, i, !1) ? p : p === "" + a ? a : p;
          }
        } else if (e.hasAttribute(s)) {
          if (Zn(t, a, i, !1))
            return e.getAttribute(s);
          if (i.type === Ln)
            return a;
          f = e.getAttribute(s);
        }
        return Zn(t, a, i, !1) ? f === null ? a : f : f === "" + a ? a : f;
      }
    }
    function ou(e, t, a, i) {
      {
        if (!en(t))
          return;
        if (!e.hasAttribute(t))
          return a === void 0 ? void 0 : null;
        var u = e.getAttribute(t);
        return In(a, t), u === "" + a ? a : u;
      }
    }
    function kr(e, t, a, i) {
      var u = tn(t);
      if (!hn(t, u, i)) {
        if (Zn(t, a, u, i) && (a = null), i || u === null) {
          if (en(t)) {
            var s = t;
            a === null ? e.removeAttribute(s) : (In(a, t), e.setAttribute(s, "" + a));
          }
          return;
        }
        var f = u.mustUseProperty;
        if (f) {
          var p = u.propertyName;
          if (a === null) {
            var v = u.type;
            e[p] = v === Ln ? !1 : "";
          } else
            e[p] = a;
          return;
        }
        var y = u.attributeName, g = u.attributeNamespace;
        if (a === null)
          e.removeAttribute(y);
        else {
          var x = u.type, b;
          x === Ln || x === Cr && a === !0 ? b = "" : (In(a, y), b = "" + a, u.sanitizeURL && El(b.toString())), g ? e.setAttributeNS(g, y, b) : e.setAttribute(y, b);
        }
      }
    }
    var Dr = Symbol.for("react.element"), ir = Symbol.for("react.portal"), mi = Symbol.for("react.fragment"), Xa = Symbol.for("react.strict_mode"), yi = Symbol.for("react.profiler"), gi = Symbol.for("react.provider"), _ = Symbol.for("react.context"), I = Symbol.for("react.forward_ref"), ue = Symbol.for("react.suspense"), ge = Symbol.for("react.suspense_list"), Ze = Symbol.for("react.memo"), We = Symbol.for("react.lazy"), pt = Symbol.for("react.scope"), st = Symbol.for("react.debug_trace_mode"), Tn = Symbol.for("react.offscreen"), nn = Symbol.for("react.legacy_hidden"), sn = Symbol.for("react.cache"), lr = Symbol.for("react.tracing_marker"), Za = Symbol.iterator, Ja = "@@iterator";
    function Je(e) {
      if (e === null || typeof e != "object")
        return null;
      var t = Za && e[Za] || e[Ja];
      return typeof t == "function" ? t : null;
    }
    var nt = Object.assign, ei = 0, su, cu, _l, eo, Rl, Gr, Zo;
    function Or() {
    }
    Or.__reactDisabledLog = !0;
    function pc() {
      {
        if (ei === 0) {
          su = console.log, cu = console.info, _l = console.warn, eo = console.error, Rl = console.group, Gr = console.groupCollapsed, Zo = console.groupEnd;
          var e = {
            configurable: !0,
            enumerable: !0,
            value: Or,
            writable: !0
          };
          Object.defineProperties(console, {
            info: e,
            log: e,
            warn: e,
            error: e,
            group: e,
            groupCollapsed: e,
            groupEnd: e
          });
        }
        ei++;
      }
    }
    function vc() {
      {
        if (ei--, ei === 0) {
          var e = {
            configurable: !0,
            enumerable: !0,
            writable: !0
          };
          Object.defineProperties(console, {
            log: nt({}, e, {
              value: su
            }),
            info: nt({}, e, {
              value: cu
            }),
            warn: nt({}, e, {
              value: _l
            }),
            error: nt({}, e, {
              value: eo
            }),
            group: nt({}, e, {
              value: Rl
            }),
            groupCollapsed: nt({}, e, {
              value: Gr
            }),
            groupEnd: nt({}, e, {
              value: Zo
            })
          });
        }
        ei < 0 && S("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
      }
    }
    var to = T.ReactCurrentDispatcher, Tl;
    function va(e, t, a) {
      {
        if (Tl === void 0)
          try {
            throw Error();
          } catch (u) {
            var i = u.stack.trim().match(/\n( *(at )?)/);
            Tl = i && i[1] || "";
          }
        return `
` + Tl + e;
      }
    }
    var ti = !1, ni;
    {
      var no = typeof WeakMap == "function" ? WeakMap : Map;
      ni = new no();
    }
    function fu(e, t) {
      if (!e || ti)
        return "";
      {
        var a = ni.get(e);
        if (a !== void 0)
          return a;
      }
      var i;
      ti = !0;
      var u = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      var s;
      s = to.current, to.current = null, pc();
      try {
        if (t) {
          var f = function() {
            throw Error();
          };
          if (Object.defineProperty(f.prototype, "props", {
            set: function() {
              throw Error();
            }
          }), typeof Reflect == "object" && Reflect.construct) {
            try {
              Reflect.construct(f, []);
            } catch (F) {
              i = F;
            }
            Reflect.construct(e, [], f);
          } else {
            try {
              f.call();
            } catch (F) {
              i = F;
            }
            e.call(f.prototype);
          }
        } else {
          try {
            throw Error();
          } catch (F) {
            i = F;
          }
          e();
        }
      } catch (F) {
        if (F && i && typeof F.stack == "string") {
          for (var p = F.stack.split(`
`), v = i.stack.split(`
`), y = p.length - 1, g = v.length - 1; y >= 1 && g >= 0 && p[y] !== v[g]; )
            g--;
          for (; y >= 1 && g >= 0; y--, g--)
            if (p[y] !== v[g]) {
              if (y !== 1 || g !== 1)
                do
                  if (y--, g--, g < 0 || p[y] !== v[g]) {
                    var x = `
` + p[y].replace(" at new ", " at ");
                    return e.displayName && x.includes("<anonymous>") && (x = x.replace("<anonymous>", e.displayName)), typeof e == "function" && ni.set(e, x), x;
                  }
                while (y >= 1 && g >= 0);
              break;
            }
        }
      } finally {
        ti = !1, to.current = s, vc(), Error.prepareStackTrace = u;
      }
      var b = e ? e.displayName || e.name : "", U = b ? va(b) : "";
      return typeof e == "function" && ni.set(e, U), U;
    }
    function bl(e, t, a) {
      return fu(e, !0);
    }
    function ro(e, t, a) {
      return fu(e, !1);
    }
    function ao(e) {
      var t = e.prototype;
      return !!(t && t.isReactComponent);
    }
    function Ii(e, t, a) {
      if (e == null)
        return "";
      if (typeof e == "function")
        return fu(e, ao(e));
      if (typeof e == "string")
        return va(e);
      switch (e) {
        case ue:
          return va("Suspense");
        case ge:
          return va("SuspenseList");
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case I:
            return ro(e.render);
          case Ze:
            return Ii(e.type, t, a);
          case We: {
            var i = e, u = i._payload, s = i._init;
            try {
              return Ii(s(u), t, a);
            } catch {
            }
          }
        }
      return "";
    }
    function Jf(e) {
      switch (e._debugOwner && e._debugOwner.type, e._debugSource, e.tag) {
        case fe:
          return va(e.type);
        case ln:
          return va("Lazy");
        case De:
          return va("Suspense");
        case un:
          return va("SuspenseList");
        case ee:
        case Ve:
        case Be:
          return ro(e.type);
        case Ke:
          return ro(e.type.render);
        case ne:
          return bl(e.type);
        default:
          return "";
      }
    }
    function Yi(e) {
      try {
        var t = "", a = e;
        do
          t += Jf(a), a = a.return;
        while (a);
        return t;
      } catch (i) {
        return `
Error generating stack: ` + i.message + `
` + i.stack;
      }
    }
    function Lt(e, t, a) {
      var i = e.displayName;
      if (i)
        return i;
      var u = t.displayName || t.name || "";
      return u !== "" ? a + "(" + u + ")" : a;
    }
    function io(e) {
      return e.displayName || "Context";
    }
    function wt(e) {
      if (e == null)
        return null;
      if (typeof e.tag == "number" && S("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof e == "function")
        return e.displayName || e.name || null;
      if (typeof e == "string")
        return e;
      switch (e) {
        case mi:
          return "Fragment";
        case ir:
          return "Portal";
        case yi:
          return "Profiler";
        case Xa:
          return "StrictMode";
        case ue:
          return "Suspense";
        case ge:
          return "SuspenseList";
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case _:
            var t = e;
            return io(t) + ".Consumer";
          case gi:
            var a = e;
            return io(a._context) + ".Provider";
          case I:
            return Lt(e, e.render, "ForwardRef");
          case Ze:
            var i = e.displayName || null;
            return i !== null ? i : wt(e.type) || "Memo";
          case We: {
            var u = e, s = u._payload, f = u._init;
            try {
              return wt(f(s));
            } catch {
              return null;
            }
          }
        }
      return null;
    }
    function Jo(e, t, a) {
      var i = t.displayName || t.name || "";
      return e.displayName || (i !== "" ? a + "(" + i + ")" : a);
    }
    function Si(e) {
      return e.displayName || "Context";
    }
    function Qe(e) {
      var t = e.tag, a = e.type;
      switch (t) {
        case Dt:
          return "Cache";
        case dn:
          var i = a;
          return Si(i) + ".Consumer";
        case ht:
          var u = a;
          return Si(u._context) + ".Provider";
        case Jt:
          return "DehydratedFragment";
        case Ke:
          return Jo(a, a.render, "ForwardRef");
        case Et:
          return "Fragment";
        case fe:
          return a;
        case me:
          return "Portal";
        case te:
          return "Root";
        case qe:
          return "Text";
        case ln:
          return wt(a);
        case mt:
          return a === Xa ? "StrictMode" : "Mode";
        case Le:
          return "Offscreen";
        case yt:
          return "Profiler";
        case kt:
          return "Scope";
        case De:
          return "Suspense";
        case un:
          return "SuspenseList";
        case Nt:
          return "TracingMarker";
        case ne:
        case ee:
        case Vt:
        case Ve:
        case dt:
        case Be:
          if (typeof a == "function")
            return a.displayName || a.name || null;
          if (typeof a == "string")
            return a;
          break;
      }
      return null;
    }
    var lo = T.ReactDebugCurrentFrame, ur = null, Ei = !1;
    function Nr() {
      {
        if (ur === null)
          return null;
        var e = ur._debugOwner;
        if (e !== null && typeof e < "u")
          return Qe(e);
      }
      return null;
    }
    function Ci() {
      return ur === null ? "" : Yi(ur);
    }
    function cn() {
      lo.getCurrentStack = null, ur = null, Ei = !1;
    }
    function Qt(e) {
      lo.getCurrentStack = e === null ? null : Ci, ur = e, Ei = !1;
    }
    function wl() {
      return ur;
    }
    function Qn(e) {
      Ei = e;
    }
    function Lr(e) {
      return "" + e;
    }
    function ka(e) {
      switch (typeof e) {
        case "boolean":
        case "number":
        case "string":
        case "undefined":
          return e;
        case "object":
          return Rn(e), e;
        default:
          return "";
      }
    }
    var du = {
      button: !0,
      checkbox: !0,
      image: !0,
      hidden: !0,
      radio: !0,
      reset: !0,
      submit: !0
    };
    function es(e, t) {
      du[t.type] || t.onChange || t.onInput || t.readOnly || t.disabled || t.value == null || S("You provided a `value` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultValue`. Otherwise, set either `onChange` or `readOnly`."), t.onChange || t.readOnly || t.disabled || t.checked == null || S("You provided a `checked` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultChecked`. Otherwise, set either `onChange` or `readOnly`.");
    }
    function ts(e) {
      var t = e.type, a = e.nodeName;
      return a && a.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
    }
    function xl(e) {
      return e._valueTracker;
    }
    function pu(e) {
      e._valueTracker = null;
    }
    function ed(e) {
      var t = "";
      return e && (ts(e) ? t = e.checked ? "true" : "false" : t = e.value), t;
    }
    function Da(e) {
      var t = ts(e) ? "checked" : "value", a = Object.getOwnPropertyDescriptor(e.constructor.prototype, t);
      Rn(e[t]);
      var i = "" + e[t];
      if (!(e.hasOwnProperty(t) || typeof a > "u" || typeof a.get != "function" || typeof a.set != "function")) {
        var u = a.get, s = a.set;
        Object.defineProperty(e, t, {
          configurable: !0,
          get: function() {
            return u.call(this);
          },
          set: function(p) {
            Rn(p), i = "" + p, s.call(this, p);
          }
        }), Object.defineProperty(e, t, {
          enumerable: a.enumerable
        });
        var f = {
          getValue: function() {
            return i;
          },
          setValue: function(p) {
            Rn(p), i = "" + p;
          },
          stopTracking: function() {
            pu(e), delete e[t];
          }
        };
        return f;
      }
    }
    function ri(e) {
      xl(e) || (e._valueTracker = Da(e));
    }
    function _i(e) {
      if (!e)
        return !1;
      var t = xl(e);
      if (!t)
        return !0;
      var a = t.getValue(), i = ed(e);
      return i !== a ? (t.setValue(i), !0) : !1;
    }
    function Oa(e) {
      if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u")
        return null;
      try {
        return e.activeElement || e.body;
      } catch {
        return e.body;
      }
    }
    var uo = !1, oo = !1, kl = !1, vu = !1;
    function so(e) {
      var t = e.type === "checkbox" || e.type === "radio";
      return t ? e.checked != null : e.value != null;
    }
    function co(e, t) {
      var a = e, i = t.checked, u = nt({}, t, {
        defaultChecked: void 0,
        defaultValue: void 0,
        value: void 0,
        checked: i ?? a._wrapperState.initialChecked
      });
      return u;
    }
    function ai(e, t) {
      es("input", t), t.checked !== void 0 && t.defaultChecked !== void 0 && !oo && (S("%s contains an input of type %s with both checked and defaultChecked props. Input elements must be either controlled or uncontrolled (specify either the checked prop, or the defaultChecked prop, but not both). Decide between using a controlled or uncontrolled input element and remove one of these props. More info: https://reactjs.org/link/controlled-components", Nr() || "A component", t.type), oo = !0), t.value !== void 0 && t.defaultValue !== void 0 && !uo && (S("%s contains an input of type %s with both value and defaultValue props. Input elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled input element and remove one of these props. More info: https://reactjs.org/link/controlled-components", Nr() || "A component", t.type), uo = !0);
      var a = e, i = t.defaultValue == null ? "" : t.defaultValue;
      a._wrapperState = {
        initialChecked: t.checked != null ? t.checked : t.defaultChecked,
        initialValue: ka(t.value != null ? t.value : i),
        controlled: so(t)
      };
    }
    function h(e, t) {
      var a = e, i = t.checked;
      i != null && kr(a, "checked", i, !1);
    }
    function C(e, t) {
      var a = e;
      {
        var i = so(t);
        !a._wrapperState.controlled && i && !vu && (S("A component is changing an uncontrolled input to be controlled. This is likely caused by the value changing from undefined to a defined value, which should not happen. Decide between using a controlled or uncontrolled input element for the lifetime of the component. More info: https://reactjs.org/link/controlled-components"), vu = !0), a._wrapperState.controlled && !i && !kl && (S("A component is changing a controlled input to be uncontrolled. This is likely caused by the value changing from a defined to undefined, which should not happen. Decide between using a controlled or uncontrolled input element for the lifetime of the component. More info: https://reactjs.org/link/controlled-components"), kl = !0);
      }
      h(e, t);
      var u = ka(t.value), s = t.type;
      if (u != null)
        s === "number" ? (u === 0 && a.value === "" || // We explicitly want to coerce to number here if possible.
        // eslint-disable-next-line
        a.value != u) && (a.value = Lr(u)) : a.value !== Lr(u) && (a.value = Lr(u));
      else if (s === "submit" || s === "reset") {
        a.removeAttribute("value");
        return;
      }
      t.hasOwnProperty("value") ? Me(a, t.type, u) : t.hasOwnProperty("defaultValue") && Me(a, t.type, ka(t.defaultValue)), t.checked == null && t.defaultChecked != null && (a.defaultChecked = !!t.defaultChecked);
    }
    function z(e, t, a) {
      var i = e;
      if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
        var u = t.type, s = u === "submit" || u === "reset";
        if (s && (t.value === void 0 || t.value === null))
          return;
        var f = Lr(i._wrapperState.initialValue);
        a || f !== i.value && (i.value = f), i.defaultValue = f;
      }
      var p = i.name;
      p !== "" && (i.name = ""), i.defaultChecked = !i.defaultChecked, i.defaultChecked = !!i._wrapperState.initialChecked, p !== "" && (i.name = p);
    }
    function H(e, t) {
      var a = e;
      C(a, t), Z(a, t);
    }
    function Z(e, t) {
      var a = t.name;
      if (t.type === "radio" && a != null) {
        for (var i = e; i.parentNode; )
          i = i.parentNode;
        In(a, "name");
        for (var u = i.querySelectorAll("input[name=" + JSON.stringify("" + a) + '][type="radio"]'), s = 0; s < u.length; s++) {
          var f = u[s];
          if (!(f === e || f.form !== e.form)) {
            var p = Hh(f);
            if (!p)
              throw new Error("ReactDOMInput: Mixing React and non-React radio inputs with the same `name` is not supported.");
            _i(f), C(f, p);
          }
        }
      }
    }
    function Me(e, t, a) {
      // Focused number inputs synchronize on blur. See ChangeEventPlugin.js
      (t !== "number" || Oa(e.ownerDocument) !== e) && (a == null ? e.defaultValue = Lr(e._wrapperState.initialValue) : e.defaultValue !== Lr(a) && (e.defaultValue = Lr(a)));
    }
    var le = !1, Ae = !1, vt = !1;
    function xt(e, t) {
      t.value == null && (typeof t.children == "object" && t.children !== null ? O.Children.forEach(t.children, function(a) {
        a != null && (typeof a == "string" || typeof a == "number" || Ae || (Ae = !0, S("Cannot infer the option value of complex children. Pass a `value` prop or use a plain string as children to <option>.")));
      }) : t.dangerouslySetInnerHTML != null && (vt || (vt = !0, S("Pass a `value` prop if you set dangerouslyInnerHTML so React knows which value should be selected.")))), t.selected != null && !le && (S("Use the `defaultValue` or `value` props on <select> instead of setting `selected` on <option>."), le = !0);
    }
    function rn(e, t) {
      t.value != null && e.setAttribute("value", Lr(ka(t.value)));
    }
    var Wt = Array.isArray;
    function lt(e) {
      return Wt(e);
    }
    var Gt;
    Gt = !1;
    function mn() {
      var e = Nr();
      return e ? `

Check the render method of \`` + e + "`." : "";
    }
    var Dl = ["value", "defaultValue"];
    function ns(e) {
      {
        es("select", e);
        for (var t = 0; t < Dl.length; t++) {
          var a = Dl[t];
          if (e[a] != null) {
            var i = lt(e[a]);
            e.multiple && !i ? S("The `%s` prop supplied to <select> must be an array if `multiple` is true.%s", a, mn()) : !e.multiple && i && S("The `%s` prop supplied to <select> must be a scalar value if `multiple` is false.%s", a, mn());
          }
        }
      }
    }
    function Qi(e, t, a, i) {
      var u = e.options;
      if (t) {
        for (var s = a, f = {}, p = 0; p < s.length; p++)
          f["$" + s[p]] = !0;
        for (var v = 0; v < u.length; v++) {
          var y = f.hasOwnProperty("$" + u[v].value);
          u[v].selected !== y && (u[v].selected = y), y && i && (u[v].defaultSelected = !0);
        }
      } else {
        for (var g = Lr(ka(a)), x = null, b = 0; b < u.length; b++) {
          if (u[b].value === g) {
            u[b].selected = !0, i && (u[b].defaultSelected = !0);
            return;
          }
          x === null && !u[b].disabled && (x = u[b]);
        }
        x !== null && (x.selected = !0);
      }
    }
    function rs(e, t) {
      return nt({}, t, {
        value: void 0
      });
    }
    function hu(e, t) {
      var a = e;
      ns(t), a._wrapperState = {
        wasMultiple: !!t.multiple
      }, t.value !== void 0 && t.defaultValue !== void 0 && !Gt && (S("Select elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled select element and remove one of these props. More info: https://reactjs.org/link/controlled-components"), Gt = !0);
    }
    function td(e, t) {
      var a = e;
      a.multiple = !!t.multiple;
      var i = t.value;
      i != null ? Qi(a, !!t.multiple, i, !1) : t.defaultValue != null && Qi(a, !!t.multiple, t.defaultValue, !0);
    }
    function hc(e, t) {
      var a = e, i = a._wrapperState.wasMultiple;
      a._wrapperState.wasMultiple = !!t.multiple;
      var u = t.value;
      u != null ? Qi(a, !!t.multiple, u, !1) : i !== !!t.multiple && (t.defaultValue != null ? Qi(a, !!t.multiple, t.defaultValue, !0) : Qi(a, !!t.multiple, t.multiple ? [] : "", !1));
    }
    function nd(e, t) {
      var a = e, i = t.value;
      i != null && Qi(a, !!t.multiple, i, !1);
    }
    var ov = !1;
    function rd(e, t) {
      var a = e;
      if (t.dangerouslySetInnerHTML != null)
        throw new Error("`dangerouslySetInnerHTML` does not make sense on <textarea>.");
      var i = nt({}, t, {
        value: void 0,
        defaultValue: void 0,
        children: Lr(a._wrapperState.initialValue)
      });
      return i;
    }
    function ad(e, t) {
      var a = e;
      es("textarea", t), t.value !== void 0 && t.defaultValue !== void 0 && !ov && (S("%s contains a textarea with both value and defaultValue props. Textarea elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled textarea and remove one of these props. More info: https://reactjs.org/link/controlled-components", Nr() || "A component"), ov = !0);
      var i = t.value;
      if (i == null) {
        var u = t.children, s = t.defaultValue;
        if (u != null) {
          S("Use the `defaultValue` or `value` props instead of setting children on <textarea>.");
          {
            if (s != null)
              throw new Error("If you supply `defaultValue` on a <textarea>, do not pass children.");
            if (lt(u)) {
              if (u.length > 1)
                throw new Error("<textarea> can only have at most one child.");
              u = u[0];
            }
            s = u;
          }
        }
        s == null && (s = ""), i = s;
      }
      a._wrapperState = {
        initialValue: ka(i)
      };
    }
    function sv(e, t) {
      var a = e, i = ka(t.value), u = ka(t.defaultValue);
      if (i != null) {
        var s = Lr(i);
        s !== a.value && (a.value = s), t.defaultValue == null && a.defaultValue !== s && (a.defaultValue = s);
      }
      u != null && (a.defaultValue = Lr(u));
    }
    function cv(e, t) {
      var a = e, i = a.textContent;
      i === a._wrapperState.initialValue && i !== "" && i !== null && (a.value = i);
    }
    function ay(e, t) {
      sv(e, t);
    }
    var Wi = "http://www.w3.org/1999/xhtml", id = "http://www.w3.org/1998/Math/MathML", ld = "http://www.w3.org/2000/svg";
    function ud(e) {
      switch (e) {
        case "svg":
          return ld;
        case "math":
          return id;
        default:
          return Wi;
      }
    }
    function od(e, t) {
      return e == null || e === Wi ? ud(t) : e === ld && t === "foreignObject" ? Wi : e;
    }
    var fv = function(e) {
      return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(t, a, i, u) {
        MSApp.execUnsafeLocalFunction(function() {
          return e(t, a, i, u);
        });
      } : e;
    }, mc, dv = fv(function(e, t) {
      if (e.namespaceURI === ld && !("innerHTML" in e)) {
        mc = mc || document.createElement("div"), mc.innerHTML = "<svg>" + t.valueOf().toString() + "</svg>";
        for (var a = mc.firstChild; e.firstChild; )
          e.removeChild(e.firstChild);
        for (; a.firstChild; )
          e.appendChild(a.firstChild);
        return;
      }
      e.innerHTML = t;
    }), qr = 1, Gi = 3, Mn = 8, qi = 9, sd = 11, fo = function(e, t) {
      if (t) {
        var a = e.firstChild;
        if (a && a === e.lastChild && a.nodeType === Gi) {
          a.nodeValue = t;
          return;
        }
      }
      e.textContent = t;
    }, as = {
      animation: ["animationDelay", "animationDirection", "animationDuration", "animationFillMode", "animationIterationCount", "animationName", "animationPlayState", "animationTimingFunction"],
      background: ["backgroundAttachment", "backgroundClip", "backgroundColor", "backgroundImage", "backgroundOrigin", "backgroundPositionX", "backgroundPositionY", "backgroundRepeat", "backgroundSize"],
      backgroundPosition: ["backgroundPositionX", "backgroundPositionY"],
      border: ["borderBottomColor", "borderBottomStyle", "borderBottomWidth", "borderImageOutset", "borderImageRepeat", "borderImageSlice", "borderImageSource", "borderImageWidth", "borderLeftColor", "borderLeftStyle", "borderLeftWidth", "borderRightColor", "borderRightStyle", "borderRightWidth", "borderTopColor", "borderTopStyle", "borderTopWidth"],
      borderBlockEnd: ["borderBlockEndColor", "borderBlockEndStyle", "borderBlockEndWidth"],
      borderBlockStart: ["borderBlockStartColor", "borderBlockStartStyle", "borderBlockStartWidth"],
      borderBottom: ["borderBottomColor", "borderBottomStyle", "borderBottomWidth"],
      borderColor: ["borderBottomColor", "borderLeftColor", "borderRightColor", "borderTopColor"],
      borderImage: ["borderImageOutset", "borderImageRepeat", "borderImageSlice", "borderImageSource", "borderImageWidth"],
      borderInlineEnd: ["borderInlineEndColor", "borderInlineEndStyle", "borderInlineEndWidth"],
      borderInlineStart: ["borderInlineStartColor", "borderInlineStartStyle", "borderInlineStartWidth"],
      borderLeft: ["borderLeftColor", "borderLeftStyle", "borderLeftWidth"],
      borderRadius: ["borderBottomLeftRadius", "borderBottomRightRadius", "borderTopLeftRadius", "borderTopRightRadius"],
      borderRight: ["borderRightColor", "borderRightStyle", "borderRightWidth"],
      borderStyle: ["borderBottomStyle", "borderLeftStyle", "borderRightStyle", "borderTopStyle"],
      borderTop: ["borderTopColor", "borderTopStyle", "borderTopWidth"],
      borderWidth: ["borderBottomWidth", "borderLeftWidth", "borderRightWidth", "borderTopWidth"],
      columnRule: ["columnRuleColor", "columnRuleStyle", "columnRuleWidth"],
      columns: ["columnCount", "columnWidth"],
      flex: ["flexBasis", "flexGrow", "flexShrink"],
      flexFlow: ["flexDirection", "flexWrap"],
      font: ["fontFamily", "fontFeatureSettings", "fontKerning", "fontLanguageOverride", "fontSize", "fontSizeAdjust", "fontStretch", "fontStyle", "fontVariant", "fontVariantAlternates", "fontVariantCaps", "fontVariantEastAsian", "fontVariantLigatures", "fontVariantNumeric", "fontVariantPosition", "fontWeight", "lineHeight"],
      fontVariant: ["fontVariantAlternates", "fontVariantCaps", "fontVariantEastAsian", "fontVariantLigatures", "fontVariantNumeric", "fontVariantPosition"],
      gap: ["columnGap", "rowGap"],
      grid: ["gridAutoColumns", "gridAutoFlow", "gridAutoRows", "gridTemplateAreas", "gridTemplateColumns", "gridTemplateRows"],
      gridArea: ["gridColumnEnd", "gridColumnStart", "gridRowEnd", "gridRowStart"],
      gridColumn: ["gridColumnEnd", "gridColumnStart"],
      gridColumnGap: ["columnGap"],
      gridGap: ["columnGap", "rowGap"],
      gridRow: ["gridRowEnd", "gridRowStart"],
      gridRowGap: ["rowGap"],
      gridTemplate: ["gridTemplateAreas", "gridTemplateColumns", "gridTemplateRows"],
      listStyle: ["listStyleImage", "listStylePosition", "listStyleType"],
      margin: ["marginBottom", "marginLeft", "marginRight", "marginTop"],
      marker: ["markerEnd", "markerMid", "markerStart"],
      mask: ["maskClip", "maskComposite", "maskImage", "maskMode", "maskOrigin", "maskPositionX", "maskPositionY", "maskRepeat", "maskSize"],
      maskPosition: ["maskPositionX", "maskPositionY"],
      outline: ["outlineColor", "outlineStyle", "outlineWidth"],
      overflow: ["overflowX", "overflowY"],
      padding: ["paddingBottom", "paddingLeft", "paddingRight", "paddingTop"],
      placeContent: ["alignContent", "justifyContent"],
      placeItems: ["alignItems", "justifyItems"],
      placeSelf: ["alignSelf", "justifySelf"],
      textDecoration: ["textDecorationColor", "textDecorationLine", "textDecorationStyle"],
      textEmphasis: ["textEmphasisColor", "textEmphasisStyle"],
      transition: ["transitionDelay", "transitionDuration", "transitionProperty", "transitionTimingFunction"],
      wordWrap: ["overflowWrap"]
    }, is = {
      animationIterationCount: !0,
      aspectRatio: !0,
      borderImageOutset: !0,
      borderImageSlice: !0,
      borderImageWidth: !0,
      boxFlex: !0,
      boxFlexGroup: !0,
      boxOrdinalGroup: !0,
      columnCount: !0,
      columns: !0,
      flex: !0,
      flexGrow: !0,
      flexPositive: !0,
      flexShrink: !0,
      flexNegative: !0,
      flexOrder: !0,
      gridArea: !0,
      gridRow: !0,
      gridRowEnd: !0,
      gridRowSpan: !0,
      gridRowStart: !0,
      gridColumn: !0,
      gridColumnEnd: !0,
      gridColumnSpan: !0,
      gridColumnStart: !0,
      fontWeight: !0,
      lineClamp: !0,
      lineHeight: !0,
      opacity: !0,
      order: !0,
      orphans: !0,
      tabSize: !0,
      widows: !0,
      zIndex: !0,
      zoom: !0,
      // SVG-related properties
      fillOpacity: !0,
      floodOpacity: !0,
      stopOpacity: !0,
      strokeDasharray: !0,
      strokeDashoffset: !0,
      strokeMiterlimit: !0,
      strokeOpacity: !0,
      strokeWidth: !0
    };
    function pv(e, t) {
      return e + t.charAt(0).toUpperCase() + t.substring(1);
    }
    var vv = ["Webkit", "ms", "Moz", "O"];
    Object.keys(is).forEach(function(e) {
      vv.forEach(function(t) {
        is[pv(t, e)] = is[e];
      });
    });
    function yc(e, t, a) {
      var i = t == null || typeof t == "boolean" || t === "";
      return i ? "" : !a && typeof t == "number" && t !== 0 && !(is.hasOwnProperty(e) && is[e]) ? t + "px" : (fa(t, e), ("" + t).trim());
    }
    var hv = /([A-Z])/g, mv = /^ms-/;
    function po(e) {
      return e.replace(hv, "-$1").toLowerCase().replace(mv, "-ms-");
    }
    var yv = function() {
    };
    {
      var iy = /^(?:webkit|moz|o)[A-Z]/, ly = /^-ms-/, gv = /-(.)/g, cd = /;\s*$/, Ri = {}, mu = {}, Sv = !1, ls = !1, uy = function(e) {
        return e.replace(gv, function(t, a) {
          return a.toUpperCase();
        });
      }, Ev = function(e) {
        Ri.hasOwnProperty(e) && Ri[e] || (Ri[e] = !0, S(
          "Unsupported style property %s. Did you mean %s?",
          e,
          // As Andi Smith suggests
          // (http://www.andismith.com/blog/2012/02/modernizr-prefixed/), an `-ms` prefix
          // is converted to lowercase `ms`.
          uy(e.replace(ly, "ms-"))
        ));
      }, fd = function(e) {
        Ri.hasOwnProperty(e) && Ri[e] || (Ri[e] = !0, S("Unsupported vendor-prefixed style property %s. Did you mean %s?", e, e.charAt(0).toUpperCase() + e.slice(1)));
      }, dd = function(e, t) {
        mu.hasOwnProperty(t) && mu[t] || (mu[t] = !0, S(`Style property values shouldn't contain a semicolon. Try "%s: %s" instead.`, e, t.replace(cd, "")));
      }, Cv = function(e, t) {
        Sv || (Sv = !0, S("`NaN` is an invalid value for the `%s` css style property.", e));
      }, _v = function(e, t) {
        ls || (ls = !0, S("`Infinity` is an invalid value for the `%s` css style property.", e));
      };
      yv = function(e, t) {
        e.indexOf("-") > -1 ? Ev(e) : iy.test(e) ? fd(e) : cd.test(t) && dd(e, t), typeof t == "number" && (isNaN(t) ? Cv(e, t) : isFinite(t) || _v(e, t));
      };
    }
    var Rv = yv;
    function oy(e) {
      {
        var t = "", a = "";
        for (var i in e)
          if (e.hasOwnProperty(i)) {
            var u = e[i];
            if (u != null) {
              var s = i.indexOf("--") === 0;
              t += a + (s ? i : po(i)) + ":", t += yc(i, u, s), a = ";";
            }
          }
        return t || null;
      }
    }
    function Tv(e, t) {
      var a = e.style;
      for (var i in t)
        if (t.hasOwnProperty(i)) {
          var u = i.indexOf("--") === 0;
          u || Rv(i, t[i]);
          var s = yc(i, t[i], u);
          i === "float" && (i = "cssFloat"), u ? a.setProperty(i, s) : a[i] = s;
        }
    }
    function sy(e) {
      return e == null || typeof e == "boolean" || e === "";
    }
    function bv(e) {
      var t = {};
      for (var a in e)
        for (var i = as[a] || [a], u = 0; u < i.length; u++)
          t[i[u]] = a;
      return t;
    }
    function cy(e, t) {
      {
        if (!t)
          return;
        var a = bv(e), i = bv(t), u = {};
        for (var s in a) {
          var f = a[s], p = i[s];
          if (p && f !== p) {
            var v = f + "," + p;
            if (u[v])
              continue;
            u[v] = !0, S("%s a style property during rerender (%s) when a conflicting property is set (%s) can lead to styling bugs. To avoid this, don't mix shorthand and non-shorthand properties for the same value; instead, replace the shorthand with separate values.", sy(e[f]) ? "Removing" : "Updating", f, p);
          }
        }
      }
    }
    var ii = {
      area: !0,
      base: !0,
      br: !0,
      col: !0,
      embed: !0,
      hr: !0,
      img: !0,
      input: !0,
      keygen: !0,
      link: !0,
      meta: !0,
      param: !0,
      source: !0,
      track: !0,
      wbr: !0
      // NOTE: menuitem's close tag should be omitted, but that causes problems.
    }, us = nt({
      menuitem: !0
    }, ii), wv = "__html";
    function gc(e, t) {
      if (t) {
        if (us[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
          throw new Error(e + " is a void element tag and must neither have `children` nor use `dangerouslySetInnerHTML`.");
        if (t.dangerouslySetInnerHTML != null) {
          if (t.children != null)
            throw new Error("Can only set one of `children` or `props.dangerouslySetInnerHTML`.");
          if (typeof t.dangerouslySetInnerHTML != "object" || !(wv in t.dangerouslySetInnerHTML))
            throw new Error("`props.dangerouslySetInnerHTML` must be in the form `{__html: ...}`. Please visit https://reactjs.org/link/dangerously-set-inner-html for more information.");
        }
        if (!t.suppressContentEditableWarning && t.contentEditable && t.children != null && S("A component is `contentEditable` and contains `children` managed by React. It is now your responsibility to guarantee that none of those nodes are unexpectedly modified or duplicated. This is probably not intentional."), t.style != null && typeof t.style != "object")
          throw new Error("The `style` prop expects a mapping from style properties to values, not a string. For example, style={{marginRight: spacing + 'em'}} when using JSX.");
      }
    }
    function Ol(e, t) {
      if (e.indexOf("-") === -1)
        return typeof t.is == "string";
      switch (e) {
        case "annotation-xml":
        case "color-profile":
        case "font-face":
        case "font-face-src":
        case "font-face-uri":
        case "font-face-format":
        case "font-face-name":
        case "missing-glyph":
          return !1;
        default:
          return !0;
      }
    }
    var os = {
      // HTML
      accept: "accept",
      acceptcharset: "acceptCharset",
      "accept-charset": "acceptCharset",
      accesskey: "accessKey",
      action: "action",
      allowfullscreen: "allowFullScreen",
      alt: "alt",
      as: "as",
      async: "async",
      autocapitalize: "autoCapitalize",
      autocomplete: "autoComplete",
      autocorrect: "autoCorrect",
      autofocus: "autoFocus",
      autoplay: "autoPlay",
      autosave: "autoSave",
      capture: "capture",
      cellpadding: "cellPadding",
      cellspacing: "cellSpacing",
      challenge: "challenge",
      charset: "charSet",
      checked: "checked",
      children: "children",
      cite: "cite",
      class: "className",
      classid: "classID",
      classname: "className",
      cols: "cols",
      colspan: "colSpan",
      content: "content",
      contenteditable: "contentEditable",
      contextmenu: "contextMenu",
      controls: "controls",
      controlslist: "controlsList",
      coords: "coords",
      crossorigin: "crossOrigin",
      dangerouslysetinnerhtml: "dangerouslySetInnerHTML",
      data: "data",
      datetime: "dateTime",
      default: "default",
      defaultchecked: "defaultChecked",
      defaultvalue: "defaultValue",
      defer: "defer",
      dir: "dir",
      disabled: "disabled",
      disablepictureinpicture: "disablePictureInPicture",
      disableremoteplayback: "disableRemotePlayback",
      download: "download",
      draggable: "draggable",
      enctype: "encType",
      enterkeyhint: "enterKeyHint",
      for: "htmlFor",
      form: "form",
      formmethod: "formMethod",
      formaction: "formAction",
      formenctype: "formEncType",
      formnovalidate: "formNoValidate",
      formtarget: "formTarget",
      frameborder: "frameBorder",
      headers: "headers",
      height: "height",
      hidden: "hidden",
      high: "high",
      href: "href",
      hreflang: "hrefLang",
      htmlfor: "htmlFor",
      httpequiv: "httpEquiv",
      "http-equiv": "httpEquiv",
      icon: "icon",
      id: "id",
      imagesizes: "imageSizes",
      imagesrcset: "imageSrcSet",
      innerhtml: "innerHTML",
      inputmode: "inputMode",
      integrity: "integrity",
      is: "is",
      itemid: "itemID",
      itemprop: "itemProp",
      itemref: "itemRef",
      itemscope: "itemScope",
      itemtype: "itemType",
      keyparams: "keyParams",
      keytype: "keyType",
      kind: "kind",
      label: "label",
      lang: "lang",
      list: "list",
      loop: "loop",
      low: "low",
      manifest: "manifest",
      marginwidth: "marginWidth",
      marginheight: "marginHeight",
      max: "max",
      maxlength: "maxLength",
      media: "media",
      mediagroup: "mediaGroup",
      method: "method",
      min: "min",
      minlength: "minLength",
      multiple: "multiple",
      muted: "muted",
      name: "name",
      nomodule: "noModule",
      nonce: "nonce",
      novalidate: "noValidate",
      open: "open",
      optimum: "optimum",
      pattern: "pattern",
      placeholder: "placeholder",
      playsinline: "playsInline",
      poster: "poster",
      preload: "preload",
      profile: "profile",
      radiogroup: "radioGroup",
      readonly: "readOnly",
      referrerpolicy: "referrerPolicy",
      rel: "rel",
      required: "required",
      reversed: "reversed",
      role: "role",
      rows: "rows",
      rowspan: "rowSpan",
      sandbox: "sandbox",
      scope: "scope",
      scoped: "scoped",
      scrolling: "scrolling",
      seamless: "seamless",
      selected: "selected",
      shape: "shape",
      size: "size",
      sizes: "sizes",
      span: "span",
      spellcheck: "spellCheck",
      src: "src",
      srcdoc: "srcDoc",
      srclang: "srcLang",
      srcset: "srcSet",
      start: "start",
      step: "step",
      style: "style",
      summary: "summary",
      tabindex: "tabIndex",
      target: "target",
      title: "title",
      type: "type",
      usemap: "useMap",
      value: "value",
      width: "width",
      wmode: "wmode",
      wrap: "wrap",
      // SVG
      about: "about",
      accentheight: "accentHeight",
      "accent-height": "accentHeight",
      accumulate: "accumulate",
      additive: "additive",
      alignmentbaseline: "alignmentBaseline",
      "alignment-baseline": "alignmentBaseline",
      allowreorder: "allowReorder",
      alphabetic: "alphabetic",
      amplitude: "amplitude",
      arabicform: "arabicForm",
      "arabic-form": "arabicForm",
      ascent: "ascent",
      attributename: "attributeName",
      attributetype: "attributeType",
      autoreverse: "autoReverse",
      azimuth: "azimuth",
      basefrequency: "baseFrequency",
      baselineshift: "baselineShift",
      "baseline-shift": "baselineShift",
      baseprofile: "baseProfile",
      bbox: "bbox",
      begin: "begin",
      bias: "bias",
      by: "by",
      calcmode: "calcMode",
      capheight: "capHeight",
      "cap-height": "capHeight",
      clip: "clip",
      clippath: "clipPath",
      "clip-path": "clipPath",
      clippathunits: "clipPathUnits",
      cliprule: "clipRule",
      "clip-rule": "clipRule",
      color: "color",
      colorinterpolation: "colorInterpolation",
      "color-interpolation": "colorInterpolation",
      colorinterpolationfilters: "colorInterpolationFilters",
      "color-interpolation-filters": "colorInterpolationFilters",
      colorprofile: "colorProfile",
      "color-profile": "colorProfile",
      colorrendering: "colorRendering",
      "color-rendering": "colorRendering",
      contentscripttype: "contentScriptType",
      contentstyletype: "contentStyleType",
      cursor: "cursor",
      cx: "cx",
      cy: "cy",
      d: "d",
      datatype: "datatype",
      decelerate: "decelerate",
      descent: "descent",
      diffuseconstant: "diffuseConstant",
      direction: "direction",
      display: "display",
      divisor: "divisor",
      dominantbaseline: "dominantBaseline",
      "dominant-baseline": "dominantBaseline",
      dur: "dur",
      dx: "dx",
      dy: "dy",
      edgemode: "edgeMode",
      elevation: "elevation",
      enablebackground: "enableBackground",
      "enable-background": "enableBackground",
      end: "end",
      exponent: "exponent",
      externalresourcesrequired: "externalResourcesRequired",
      fill: "fill",
      fillopacity: "fillOpacity",
      "fill-opacity": "fillOpacity",
      fillrule: "fillRule",
      "fill-rule": "fillRule",
      filter: "filter",
      filterres: "filterRes",
      filterunits: "filterUnits",
      floodopacity: "floodOpacity",
      "flood-opacity": "floodOpacity",
      floodcolor: "floodColor",
      "flood-color": "floodColor",
      focusable: "focusable",
      fontfamily: "fontFamily",
      "font-family": "fontFamily",
      fontsize: "fontSize",
      "font-size": "fontSize",
      fontsizeadjust: "fontSizeAdjust",
      "font-size-adjust": "fontSizeAdjust",
      fontstretch: "fontStretch",
      "font-stretch": "fontStretch",
      fontstyle: "fontStyle",
      "font-style": "fontStyle",
      fontvariant: "fontVariant",
      "font-variant": "fontVariant",
      fontweight: "fontWeight",
      "font-weight": "fontWeight",
      format: "format",
      from: "from",
      fx: "fx",
      fy: "fy",
      g1: "g1",
      g2: "g2",
      glyphname: "glyphName",
      "glyph-name": "glyphName",
      glyphorientationhorizontal: "glyphOrientationHorizontal",
      "glyph-orientation-horizontal": "glyphOrientationHorizontal",
      glyphorientationvertical: "glyphOrientationVertical",
      "glyph-orientation-vertical": "glyphOrientationVertical",
      glyphref: "glyphRef",
      gradienttransform: "gradientTransform",
      gradientunits: "gradientUnits",
      hanging: "hanging",
      horizadvx: "horizAdvX",
      "horiz-adv-x": "horizAdvX",
      horizoriginx: "horizOriginX",
      "horiz-origin-x": "horizOriginX",
      ideographic: "ideographic",
      imagerendering: "imageRendering",
      "image-rendering": "imageRendering",
      in2: "in2",
      in: "in",
      inlist: "inlist",
      intercept: "intercept",
      k1: "k1",
      k2: "k2",
      k3: "k3",
      k4: "k4",
      k: "k",
      kernelmatrix: "kernelMatrix",
      kernelunitlength: "kernelUnitLength",
      kerning: "kerning",
      keypoints: "keyPoints",
      keysplines: "keySplines",
      keytimes: "keyTimes",
      lengthadjust: "lengthAdjust",
      letterspacing: "letterSpacing",
      "letter-spacing": "letterSpacing",
      lightingcolor: "lightingColor",
      "lighting-color": "lightingColor",
      limitingconeangle: "limitingConeAngle",
      local: "local",
      markerend: "markerEnd",
      "marker-end": "markerEnd",
      markerheight: "markerHeight",
      markermid: "markerMid",
      "marker-mid": "markerMid",
      markerstart: "markerStart",
      "marker-start": "markerStart",
      markerunits: "markerUnits",
      markerwidth: "markerWidth",
      mask: "mask",
      maskcontentunits: "maskContentUnits",
      maskunits: "maskUnits",
      mathematical: "mathematical",
      mode: "mode",
      numoctaves: "numOctaves",
      offset: "offset",
      opacity: "opacity",
      operator: "operator",
      order: "order",
      orient: "orient",
      orientation: "orientation",
      origin: "origin",
      overflow: "overflow",
      overlineposition: "overlinePosition",
      "overline-position": "overlinePosition",
      overlinethickness: "overlineThickness",
      "overline-thickness": "overlineThickness",
      paintorder: "paintOrder",
      "paint-order": "paintOrder",
      panose1: "panose1",
      "panose-1": "panose1",
      pathlength: "pathLength",
      patterncontentunits: "patternContentUnits",
      patterntransform: "patternTransform",
      patternunits: "patternUnits",
      pointerevents: "pointerEvents",
      "pointer-events": "pointerEvents",
      points: "points",
      pointsatx: "pointsAtX",
      pointsaty: "pointsAtY",
      pointsatz: "pointsAtZ",
      prefix: "prefix",
      preservealpha: "preserveAlpha",
      preserveaspectratio: "preserveAspectRatio",
      primitiveunits: "primitiveUnits",
      property: "property",
      r: "r",
      radius: "radius",
      refx: "refX",
      refy: "refY",
      renderingintent: "renderingIntent",
      "rendering-intent": "renderingIntent",
      repeatcount: "repeatCount",
      repeatdur: "repeatDur",
      requiredextensions: "requiredExtensions",
      requiredfeatures: "requiredFeatures",
      resource: "resource",
      restart: "restart",
      result: "result",
      results: "results",
      rotate: "rotate",
      rx: "rx",
      ry: "ry",
      scale: "scale",
      security: "security",
      seed: "seed",
      shaperendering: "shapeRendering",
      "shape-rendering": "shapeRendering",
      slope: "slope",
      spacing: "spacing",
      specularconstant: "specularConstant",
      specularexponent: "specularExponent",
      speed: "speed",
      spreadmethod: "spreadMethod",
      startoffset: "startOffset",
      stddeviation: "stdDeviation",
      stemh: "stemh",
      stemv: "stemv",
      stitchtiles: "stitchTiles",
      stopcolor: "stopColor",
      "stop-color": "stopColor",
      stopopacity: "stopOpacity",
      "stop-opacity": "stopOpacity",
      strikethroughposition: "strikethroughPosition",
      "strikethrough-position": "strikethroughPosition",
      strikethroughthickness: "strikethroughThickness",
      "strikethrough-thickness": "strikethroughThickness",
      string: "string",
      stroke: "stroke",
      strokedasharray: "strokeDasharray",
      "stroke-dasharray": "strokeDasharray",
      strokedashoffset: "strokeDashoffset",
      "stroke-dashoffset": "strokeDashoffset",
      strokelinecap: "strokeLinecap",
      "stroke-linecap": "strokeLinecap",
      strokelinejoin: "strokeLinejoin",
      "stroke-linejoin": "strokeLinejoin",
      strokemiterlimit: "strokeMiterlimit",
      "stroke-miterlimit": "strokeMiterlimit",
      strokewidth: "strokeWidth",
      "stroke-width": "strokeWidth",
      strokeopacity: "strokeOpacity",
      "stroke-opacity": "strokeOpacity",
      suppresscontenteditablewarning: "suppressContentEditableWarning",
      suppresshydrationwarning: "suppressHydrationWarning",
      surfacescale: "surfaceScale",
      systemlanguage: "systemLanguage",
      tablevalues: "tableValues",
      targetx: "targetX",
      targety: "targetY",
      textanchor: "textAnchor",
      "text-anchor": "textAnchor",
      textdecoration: "textDecoration",
      "text-decoration": "textDecoration",
      textlength: "textLength",
      textrendering: "textRendering",
      "text-rendering": "textRendering",
      to: "to",
      transform: "transform",
      typeof: "typeof",
      u1: "u1",
      u2: "u2",
      underlineposition: "underlinePosition",
      "underline-position": "underlinePosition",
      underlinethickness: "underlineThickness",
      "underline-thickness": "underlineThickness",
      unicode: "unicode",
      unicodebidi: "unicodeBidi",
      "unicode-bidi": "unicodeBidi",
      unicoderange: "unicodeRange",
      "unicode-range": "unicodeRange",
      unitsperem: "unitsPerEm",
      "units-per-em": "unitsPerEm",
      unselectable: "unselectable",
      valphabetic: "vAlphabetic",
      "v-alphabetic": "vAlphabetic",
      values: "values",
      vectoreffect: "vectorEffect",
      "vector-effect": "vectorEffect",
      version: "version",
      vertadvy: "vertAdvY",
      "vert-adv-y": "vertAdvY",
      vertoriginx: "vertOriginX",
      "vert-origin-x": "vertOriginX",
      vertoriginy: "vertOriginY",
      "vert-origin-y": "vertOriginY",
      vhanging: "vHanging",
      "v-hanging": "vHanging",
      videographic: "vIdeographic",
      "v-ideographic": "vIdeographic",
      viewbox: "viewBox",
      viewtarget: "viewTarget",
      visibility: "visibility",
      vmathematical: "vMathematical",
      "v-mathematical": "vMathematical",
      vocab: "vocab",
      widths: "widths",
      wordspacing: "wordSpacing",
      "word-spacing": "wordSpacing",
      writingmode: "writingMode",
      "writing-mode": "writingMode",
      x1: "x1",
      x2: "x2",
      x: "x",
      xchannelselector: "xChannelSelector",
      xheight: "xHeight",
      "x-height": "xHeight",
      xlinkactuate: "xlinkActuate",
      "xlink:actuate": "xlinkActuate",
      xlinkarcrole: "xlinkArcrole",
      "xlink:arcrole": "xlinkArcrole",
      xlinkhref: "xlinkHref",
      "xlink:href": "xlinkHref",
      xlinkrole: "xlinkRole",
      "xlink:role": "xlinkRole",
      xlinkshow: "xlinkShow",
      "xlink:show": "xlinkShow",
      xlinktitle: "xlinkTitle",
      "xlink:title": "xlinkTitle",
      xlinktype: "xlinkType",
      "xlink:type": "xlinkType",
      xmlbase: "xmlBase",
      "xml:base": "xmlBase",
      xmllang: "xmlLang",
      "xml:lang": "xmlLang",
      xmlns: "xmlns",
      "xml:space": "xmlSpace",
      xmlnsxlink: "xmlnsXlink",
      "xmlns:xlink": "xmlnsXlink",
      xmlspace: "xmlSpace",
      y1: "y1",
      y2: "y2",
      y: "y",
      ychannelselector: "yChannelSelector",
      z: "z",
      zoomandpan: "zoomAndPan"
    }, Sc = {
      "aria-current": 0,
      // state
      "aria-description": 0,
      "aria-details": 0,
      "aria-disabled": 0,
      // state
      "aria-hidden": 0,
      // state
      "aria-invalid": 0,
      // state
      "aria-keyshortcuts": 0,
      "aria-label": 0,
      "aria-roledescription": 0,
      // Widget Attributes
      "aria-autocomplete": 0,
      "aria-checked": 0,
      "aria-expanded": 0,
      "aria-haspopup": 0,
      "aria-level": 0,
      "aria-modal": 0,
      "aria-multiline": 0,
      "aria-multiselectable": 0,
      "aria-orientation": 0,
      "aria-placeholder": 0,
      "aria-pressed": 0,
      "aria-readonly": 0,
      "aria-required": 0,
      "aria-selected": 0,
      "aria-sort": 0,
      "aria-valuemax": 0,
      "aria-valuemin": 0,
      "aria-valuenow": 0,
      "aria-valuetext": 0,
      // Live Region Attributes
      "aria-atomic": 0,
      "aria-busy": 0,
      "aria-live": 0,
      "aria-relevant": 0,
      // Drag-and-Drop Attributes
      "aria-dropeffect": 0,
      "aria-grabbed": 0,
      // Relationship Attributes
      "aria-activedescendant": 0,
      "aria-colcount": 0,
      "aria-colindex": 0,
      "aria-colspan": 0,
      "aria-controls": 0,
      "aria-describedby": 0,
      "aria-errormessage": 0,
      "aria-flowto": 0,
      "aria-labelledby": 0,
      "aria-owns": 0,
      "aria-posinset": 0,
      "aria-rowcount": 0,
      "aria-rowindex": 0,
      "aria-rowspan": 0,
      "aria-setsize": 0
    }, vo = {}, fy = new RegExp("^(aria)-[" + re + "]*$"), ho = new RegExp("^(aria)[A-Z][" + re + "]*$");
    function pd(e, t) {
      {
        if (xr.call(vo, t) && vo[t])
          return !0;
        if (ho.test(t)) {
          var a = "aria-" + t.slice(4).toLowerCase(), i = Sc.hasOwnProperty(a) ? a : null;
          if (i == null)
            return S("Invalid ARIA attribute `%s`. ARIA attributes follow the pattern aria-* and must be lowercase.", t), vo[t] = !0, !0;
          if (t !== i)
            return S("Invalid ARIA attribute `%s`. Did you mean `%s`?", t, i), vo[t] = !0, !0;
        }
        if (fy.test(t)) {
          var u = t.toLowerCase(), s = Sc.hasOwnProperty(u) ? u : null;
          if (s == null)
            return vo[t] = !0, !1;
          if (t !== s)
            return S("Unknown ARIA attribute `%s`. Did you mean `%s`?", t, s), vo[t] = !0, !0;
        }
      }
      return !0;
    }
    function ss(e, t) {
      {
        var a = [];
        for (var i in t) {
          var u = pd(e, i);
          u || a.push(i);
        }
        var s = a.map(function(f) {
          return "`" + f + "`";
        }).join(", ");
        a.length === 1 ? S("Invalid aria prop %s on <%s> tag. For details, see https://reactjs.org/link/invalid-aria-props", s, e) : a.length > 1 && S("Invalid aria props %s on <%s> tag. For details, see https://reactjs.org/link/invalid-aria-props", s, e);
      }
    }
    function vd(e, t) {
      Ol(e, t) || ss(e, t);
    }
    var hd = !1;
    function Ec(e, t) {
      {
        if (e !== "input" && e !== "textarea" && e !== "select")
          return;
        t != null && t.value === null && !hd && (hd = !0, e === "select" && t.multiple ? S("`value` prop on `%s` should not be null. Consider using an empty array when `multiple` is set to `true` to clear the component or `undefined` for uncontrolled components.", e) : S("`value` prop on `%s` should not be null. Consider using an empty string to clear the component or `undefined` for uncontrolled components.", e));
      }
    }
    var yu = function() {
    };
    {
      var or = {}, md = /^on./, Cc = /^on[^A-Z]/, xv = new RegExp("^(aria)-[" + re + "]*$"), kv = new RegExp("^(aria)[A-Z][" + re + "]*$");
      yu = function(e, t, a, i) {
        if (xr.call(or, t) && or[t])
          return !0;
        var u = t.toLowerCase();
        if (u === "onfocusin" || u === "onfocusout")
          return S("React uses onFocus and onBlur instead of onFocusIn and onFocusOut. All React events are normalized to bubble, so onFocusIn and onFocusOut are not needed/supported by React."), or[t] = !0, !0;
        if (i != null) {
          var s = i.registrationNameDependencies, f = i.possibleRegistrationNames;
          if (s.hasOwnProperty(t))
            return !0;
          var p = f.hasOwnProperty(u) ? f[u] : null;
          if (p != null)
            return S("Invalid event handler property `%s`. Did you mean `%s`?", t, p), or[t] = !0, !0;
          if (md.test(t))
            return S("Unknown event handler property `%s`. It will be ignored.", t), or[t] = !0, !0;
        } else if (md.test(t))
          return Cc.test(t) && S("Invalid event handler property `%s`. React events use the camelCase naming convention, for example `onClick`.", t), or[t] = !0, !0;
        if (xv.test(t) || kv.test(t))
          return !0;
        if (u === "innerhtml")
          return S("Directly setting property `innerHTML` is not permitted. For more information, lookup documentation on `dangerouslySetInnerHTML`."), or[t] = !0, !0;
        if (u === "aria")
          return S("The `aria` attribute is reserved for future use in React. Pass individual `aria-` attributes instead."), or[t] = !0, !0;
        if (u === "is" && a !== null && a !== void 0 && typeof a != "string")
          return S("Received a `%s` for a string attribute `is`. If this is expected, cast the value to a string.", typeof a), or[t] = !0, !0;
        if (typeof a == "number" && isNaN(a))
          return S("Received NaN for the `%s` attribute. If this is expected, cast the value to a string.", t), or[t] = !0, !0;
        var v = tn(t), y = v !== null && v.type === Yn;
        if (os.hasOwnProperty(u)) {
          var g = os[u];
          if (g !== t)
            return S("Invalid DOM property `%s`. Did you mean `%s`?", t, g), or[t] = !0, !0;
        } else if (!y && t !== u)
          return S("React does not recognize the `%s` prop on a DOM element. If you intentionally want it to appear in the DOM as a custom attribute, spell it as lowercase `%s` instead. If you accidentally passed it from a parent component, remove it from the DOM element.", t, u), or[t] = !0, !0;
        return typeof a == "boolean" && on(t, a, v, !1) ? (a ? S('Received `%s` for a non-boolean attribute `%s`.\n\nIf you want to write it to the DOM, pass a string instead: %s="%s" or %s={value.toString()}.', a, t, t, a, t) : S('Received `%s` for a non-boolean attribute `%s`.\n\nIf you want to write it to the DOM, pass a string instead: %s="%s" or %s={value.toString()}.\n\nIf you used to conditionally omit it with %s={condition && value}, pass %s={condition ? value : undefined} instead.', a, t, t, a, t, t, t), or[t] = !0, !0) : y ? !0 : on(t, a, v, !1) ? (or[t] = !0, !1) : ((a === "false" || a === "true") && v !== null && v.type === Ln && (S("Received the string `%s` for the boolean attribute `%s`. %s Did you mean %s={%s}?", a, t, a === "false" ? "The browser will interpret it as a truthy value." : 'Although this works, it will not work as expected if you pass the string "false".', t, a), or[t] = !0), !0);
      };
    }
    var Dv = function(e, t, a) {
      {
        var i = [];
        for (var u in t) {
          var s = yu(e, u, t[u], a);
          s || i.push(u);
        }
        var f = i.map(function(p) {
          return "`" + p + "`";
        }).join(", ");
        i.length === 1 ? S("Invalid value for prop %s on <%s> tag. Either remove it from the element, or pass a string or number value to keep it in the DOM. For details, see https://reactjs.org/link/attribute-behavior ", f, e) : i.length > 1 && S("Invalid values for props %s on <%s> tag. Either remove them from the element, or pass a string or number value to keep them in the DOM. For details, see https://reactjs.org/link/attribute-behavior ", f, e);
      }
    };
    function Ov(e, t, a) {
      Ol(e, t) || Dv(e, t, a);
    }
    var yd = 1, _c = 2, Na = 4, gd = yd | _c | Na, gu = null;
    function dy(e) {
      gu !== null && S("Expected currently replaying event to be null. This error is likely caused by a bug in React. Please file an issue."), gu = e;
    }
    function py() {
      gu === null && S("Expected currently replaying event to not be null. This error is likely caused by a bug in React. Please file an issue."), gu = null;
    }
    function cs(e) {
      return e === gu;
    }
    function Sd(e) {
      var t = e.target || e.srcElement || window;
      return t.correspondingUseElement && (t = t.correspondingUseElement), t.nodeType === Gi ? t.parentNode : t;
    }
    var Rc = null, Su = null, Pt = null;
    function Tc(e) {
      var t = Ao(e);
      if (t) {
        if (typeof Rc != "function")
          throw new Error("setRestoreImplementation() needs to be called to handle a target for controlled events. This error is likely caused by a bug in React. Please file an issue.");
        var a = t.stateNode;
        if (a) {
          var i = Hh(a);
          Rc(t.stateNode, t.type, i);
        }
      }
    }
    function bc(e) {
      Rc = e;
    }
    function mo(e) {
      Su ? Pt ? Pt.push(e) : Pt = [e] : Su = e;
    }
    function Nv() {
      return Su !== null || Pt !== null;
    }
    function wc() {
      if (Su) {
        var e = Su, t = Pt;
        if (Su = null, Pt = null, Tc(e), t)
          for (var a = 0; a < t.length; a++)
            Tc(t[a]);
      }
    }
    var yo = function(e, t) {
      return e(t);
    }, fs = function() {
    }, Nl = !1;
    function Lv() {
      var e = Nv();
      e && (fs(), wc());
    }
    function Mv(e, t, a) {
      if (Nl)
        return e(t, a);
      Nl = !0;
      try {
        return yo(e, t, a);
      } finally {
        Nl = !1, Lv();
      }
    }
    function vy(e, t, a) {
      yo = e, fs = a;
    }
    function Uv(e) {
      return e === "button" || e === "input" || e === "select" || e === "textarea";
    }
    function xc(e, t, a) {
      switch (e) {
        case "onClick":
        case "onClickCapture":
        case "onDoubleClick":
        case "onDoubleClickCapture":
        case "onMouseDown":
        case "onMouseDownCapture":
        case "onMouseMove":
        case "onMouseMoveCapture":
        case "onMouseUp":
        case "onMouseUpCapture":
        case "onMouseEnter":
          return !!(a.disabled && Uv(t));
        default:
          return !1;
      }
    }
    function Ll(e, t) {
      var a = e.stateNode;
      if (a === null)
        return null;
      var i = Hh(a);
      if (i === null)
        return null;
      var u = i[t];
      if (xc(t, e.type, i))
        return null;
      if (u && typeof u != "function")
        throw new Error("Expected `" + t + "` listener to be a function, instead got a value of `" + typeof u + "` type.");
      return u;
    }
    var ds = !1;
    if (Nn)
      try {
        var Eu = {};
        Object.defineProperty(Eu, "passive", {
          get: function() {
            ds = !0;
          }
        }), window.addEventListener("test", Eu, Eu), window.removeEventListener("test", Eu, Eu);
      } catch {
        ds = !1;
      }
    function kc(e, t, a, i, u, s, f, p, v) {
      var y = Array.prototype.slice.call(arguments, 3);
      try {
        t.apply(a, y);
      } catch (g) {
        this.onError(g);
      }
    }
    var Dc = kc;
    if (typeof window < "u" && typeof window.dispatchEvent == "function" && typeof document < "u" && typeof document.createEvent == "function") {
      var Ed = document.createElement("react");
      Dc = function(t, a, i, u, s, f, p, v, y) {
        if (typeof document > "u" || document === null)
          throw new Error("The `document` global was defined when React was initialized, but is not defined anymore. This can happen in a test environment if a component schedules an update from an asynchronous callback, but the test has already finished running. To solve this, you can either unmount the component at the end of your test (and ensure that any asynchronous operations get canceled in `componentWillUnmount`), or you can change the test itself to be asynchronous.");
        var g = document.createEvent("Event"), x = !1, b = !0, U = window.event, F = Object.getOwnPropertyDescriptor(window, "event");
        function V() {
          Ed.removeEventListener(P, Ue, !1), typeof window.event < "u" && window.hasOwnProperty("event") && (window.event = U);
        }
        var ce = Array.prototype.slice.call(arguments, 3);
        function Ue() {
          x = !0, V(), a.apply(i, ce), b = !1;
        }
        var we, Tt = !1, gt = !1;
        function N(L) {
          if (we = L.error, Tt = !0, we === null && L.colno === 0 && L.lineno === 0 && (gt = !0), L.defaultPrevented && we != null && typeof we == "object")
            try {
              we._suppressLogging = !0;
            } catch {
            }
        }
        var P = "react-" + (t || "invokeguardedcallback");
        if (window.addEventListener("error", N), Ed.addEventListener(P, Ue, !1), g.initEvent(P, !1, !1), Ed.dispatchEvent(g), F && Object.defineProperty(window, "event", F), x && b && (Tt ? gt && (we = new Error("A cross-origin error was thrown. React doesn't have access to the actual error object in development. See https://reactjs.org/link/crossorigin-error for more information.")) : we = new Error(`An error was thrown inside one of your components, but React doesn't know what it was. This is likely due to browser flakiness. React does its best to preserve the "Pause on exceptions" behavior of the DevTools, which requires some DEV-mode only tricks. It's possible that these don't work in your browser. Try triggering the error in production mode, or switching to a modern browser. If you suspect that this is actually an issue with React, please file an issue.`), this.onError(we)), window.removeEventListener("error", N), !x)
          return V(), kc.apply(this, arguments);
      };
    }
    var zv = Dc, go = !1, Oc = null, So = !1, Ti = null, Av = {
      onError: function(e) {
        go = !0, Oc = e;
      }
    };
    function Ml(e, t, a, i, u, s, f, p, v) {
      go = !1, Oc = null, zv.apply(Av, arguments);
    }
    function bi(e, t, a, i, u, s, f, p, v) {
      if (Ml.apply(this, arguments), go) {
        var y = vs();
        So || (So = !0, Ti = y);
      }
    }
    function ps() {
      if (So) {
        var e = Ti;
        throw So = !1, Ti = null, e;
      }
    }
    function Ki() {
      return go;
    }
    function vs() {
      if (go) {
        var e = Oc;
        return go = !1, Oc = null, e;
      } else
        throw new Error("clearCaughtError was called but no error was captured. This error is likely caused by a bug in React. Please file an issue.");
    }
    function Eo(e) {
      return e._reactInternals;
    }
    function hy(e) {
      return e._reactInternals !== void 0;
    }
    function Cu(e, t) {
      e._reactInternals = t;
    }
    var Oe = (
      /*                      */
      0
    ), li = (
      /*                */
      1
    ), yn = (
      /*                    */
      2
    ), Ct = (
      /*                       */
      4
    ), La = (
      /*                */
      16
    ), Ma = (
      /*                 */
      32
    ), an = (
      /*                     */
      64
    ), xe = (
      /*                   */
      128
    ), Rr = (
      /*            */
      256
    ), Cn = (
      /*                          */
      512
    ), Wn = (
      /*                     */
      1024
    ), Kr = (
      /*                      */
      2048
    ), Xr = (
      /*                    */
      4096
    ), Un = (
      /*                   */
      8192
    ), Co = (
      /*             */
      16384
    ), jv = (
      /*               */
      32767
    ), hs = (
      /*                   */
      32768
    ), Jn = (
      /*                */
      65536
    ), Nc = (
      /* */
      131072
    ), wi = (
      /*                       */
      1048576
    ), _o = (
      /*                    */
      2097152
    ), Xi = (
      /*                 */
      4194304
    ), Lc = (
      /*                */
      8388608
    ), Ul = (
      /*               */
      16777216
    ), xi = (
      /*              */
      33554432
    ), zl = (
      // TODO: Remove Update flag from before mutation phase by re-landing Visibility
      // flag logic (see #20043)
      Ct | Wn | 0
    ), Al = yn | Ct | La | Ma | Cn | Xr | Un, jl = Ct | an | Cn | Un, Zi = Kr | La, zn = Xi | Lc | _o, Ua = T.ReactCurrentOwner;
    function ha(e) {
      var t = e, a = e;
      if (e.alternate)
        for (; t.return; )
          t = t.return;
      else {
        var i = t;
        do
          t = i, (t.flags & (yn | Xr)) !== Oe && (a = t.return), i = t.return;
        while (i);
      }
      return t.tag === te ? a : null;
    }
    function ki(e) {
      if (e.tag === De) {
        var t = e.memoizedState;
        if (t === null) {
          var a = e.alternate;
          a !== null && (t = a.memoizedState);
        }
        if (t !== null)
          return t.dehydrated;
      }
      return null;
    }
    function Di(e) {
      return e.tag === te ? e.stateNode.containerInfo : null;
    }
    function _u(e) {
      return ha(e) === e;
    }
    function Fv(e) {
      {
        var t = Ua.current;
        if (t !== null && t.tag === ne) {
          var a = t, i = a.stateNode;
          i._warnedAboutRefsInRender || S("%s is accessing isMounted inside its render() function. render() should be a pure function of props and state. It should never access something that requires stale data from the previous render, such as refs. Move this logic to componentDidMount and componentDidUpdate instead.", Qe(a) || "A component"), i._warnedAboutRefsInRender = !0;
        }
      }
      var u = Eo(e);
      return u ? ha(u) === u : !1;
    }
    function Mc(e) {
      if (ha(e) !== e)
        throw new Error("Unable to find node on an unmounted component.");
    }
    function Uc(e) {
      var t = e.alternate;
      if (!t) {
        var a = ha(e);
        if (a === null)
          throw new Error("Unable to find node on an unmounted component.");
        return a !== e ? null : e;
      }
      for (var i = e, u = t; ; ) {
        var s = i.return;
        if (s === null)
          break;
        var f = s.alternate;
        if (f === null) {
          var p = s.return;
          if (p !== null) {
            i = u = p;
            continue;
          }
          break;
        }
        if (s.child === f.child) {
          for (var v = s.child; v; ) {
            if (v === i)
              return Mc(s), e;
            if (v === u)
              return Mc(s), t;
            v = v.sibling;
          }
          throw new Error("Unable to find node on an unmounted component.");
        }
        if (i.return !== u.return)
          i = s, u = f;
        else {
          for (var y = !1, g = s.child; g; ) {
            if (g === i) {
              y = !0, i = s, u = f;
              break;
            }
            if (g === u) {
              y = !0, u = s, i = f;
              break;
            }
            g = g.sibling;
          }
          if (!y) {
            for (g = f.child; g; ) {
              if (g === i) {
                y = !0, i = f, u = s;
                break;
              }
              if (g === u) {
                y = !0, u = f, i = s;
                break;
              }
              g = g.sibling;
            }
            if (!y)
              throw new Error("Child was not found in either parent set. This indicates a bug in React related to the return pointer. Please file an issue.");
          }
        }
        if (i.alternate !== u)
          throw new Error("Return fibers should always be each others' alternates. This error is likely caused by a bug in React. Please file an issue.");
      }
      if (i.tag !== te)
        throw new Error("Unable to find node on an unmounted component.");
      return i.stateNode.current === i ? e : t;
    }
    function Zr(e) {
      var t = Uc(e);
      return t !== null ? Jr(t) : null;
    }
    function Jr(e) {
      if (e.tag === fe || e.tag === qe)
        return e;
      for (var t = e.child; t !== null; ) {
        var a = Jr(t);
        if (a !== null)
          return a;
        t = t.sibling;
      }
      return null;
    }
    function pn(e) {
      var t = Uc(e);
      return t !== null ? za(t) : null;
    }
    function za(e) {
      if (e.tag === fe || e.tag === qe)
        return e;
      for (var t = e.child; t !== null; ) {
        if (t.tag !== me) {
          var a = za(t);
          if (a !== null)
            return a;
        }
        t = t.sibling;
      }
      return null;
    }
    var Cd = A.unstable_scheduleCallback, Hv = A.unstable_cancelCallback, _d = A.unstable_shouldYield, Rd = A.unstable_requestPaint, Gn = A.unstable_now, zc = A.unstable_getCurrentPriorityLevel, ms = A.unstable_ImmediatePriority, Fl = A.unstable_UserBlockingPriority, Ji = A.unstable_NormalPriority, my = A.unstable_LowPriority, Ru = A.unstable_IdlePriority, Ac = A.unstable_yieldValue, Vv = A.unstable_setDisableYieldValue, Tu = null, bn = null, se = null, ma = !1, ea = typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u";
    function Ro(e) {
      if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u")
        return !1;
      var t = __REACT_DEVTOOLS_GLOBAL_HOOK__;
      if (t.isDisabled)
        return !0;
      if (!t.supportsFiber)
        return S("The installed version of React DevTools is too old and will not work with the current version of React. Please update React DevTools. https://reactjs.org/link/react-devtools"), !0;
      try {
        $e && (e = nt({}, e, {
          getLaneLabelMap: bu,
          injectProfilingHooks: Aa
        })), Tu = t.inject(e), bn = t;
      } catch (a) {
        S("React instrumentation encountered an error: %s.", a);
      }
      return !!t.checkDCE;
    }
    function Td(e, t) {
      if (bn && typeof bn.onScheduleFiberRoot == "function")
        try {
          bn.onScheduleFiberRoot(Tu, e, t);
        } catch (a) {
          ma || (ma = !0, S("React instrumentation encountered an error: %s", a));
        }
    }
    function bd(e, t) {
      if (bn && typeof bn.onCommitFiberRoot == "function")
        try {
          var a = (e.current.flags & xe) === xe;
          if (Fe) {
            var i;
            switch (t) {
              case Mr:
                i = ms;
                break;
              case Ni:
                i = Fl;
                break;
              case ja:
                i = Ji;
                break;
              case Fa:
                i = Ru;
                break;
              default:
                i = Ji;
                break;
            }
            bn.onCommitFiberRoot(Tu, e, i, a);
          }
        } catch (u) {
          ma || (ma = !0, S("React instrumentation encountered an error: %s", u));
        }
    }
    function wd(e) {
      if (bn && typeof bn.onPostCommitFiberRoot == "function")
        try {
          bn.onPostCommitFiberRoot(Tu, e);
        } catch (t) {
          ma || (ma = !0, S("React instrumentation encountered an error: %s", t));
        }
    }
    function xd(e) {
      if (bn && typeof bn.onCommitFiberUnmount == "function")
        try {
          bn.onCommitFiberUnmount(Tu, e);
        } catch (t) {
          ma || (ma = !0, S("React instrumentation encountered an error: %s", t));
        }
    }
    function gn(e) {
      if (typeof Ac == "function" && (Vv(e), ke(e)), bn && typeof bn.setStrictMode == "function")
        try {
          bn.setStrictMode(Tu, e);
        } catch (t) {
          ma || (ma = !0, S("React instrumentation encountered an error: %s", t));
        }
    }
    function Aa(e) {
      se = e;
    }
    function bu() {
      {
        for (var e = /* @__PURE__ */ new Map(), t = 1, a = 0; a < ku; a++) {
          var i = Iv(t);
          e.set(t, i), t *= 2;
        }
        return e;
      }
    }
    function kd(e) {
      se !== null && typeof se.markCommitStarted == "function" && se.markCommitStarted(e);
    }
    function Dd() {
      se !== null && typeof se.markCommitStopped == "function" && se.markCommitStopped();
    }
    function ya(e) {
      se !== null && typeof se.markComponentRenderStarted == "function" && se.markComponentRenderStarted(e);
    }
    function ga() {
      se !== null && typeof se.markComponentRenderStopped == "function" && se.markComponentRenderStopped();
    }
    function Od(e) {
      se !== null && typeof se.markComponentPassiveEffectMountStarted == "function" && se.markComponentPassiveEffectMountStarted(e);
    }
    function Pv() {
      se !== null && typeof se.markComponentPassiveEffectMountStopped == "function" && se.markComponentPassiveEffectMountStopped();
    }
    function el(e) {
      se !== null && typeof se.markComponentPassiveEffectUnmountStarted == "function" && se.markComponentPassiveEffectUnmountStarted(e);
    }
    function Hl() {
      se !== null && typeof se.markComponentPassiveEffectUnmountStopped == "function" && se.markComponentPassiveEffectUnmountStopped();
    }
    function jc(e) {
      se !== null && typeof se.markComponentLayoutEffectMountStarted == "function" && se.markComponentLayoutEffectMountStarted(e);
    }
    function Bv() {
      se !== null && typeof se.markComponentLayoutEffectMountStopped == "function" && se.markComponentLayoutEffectMountStopped();
    }
    function ys(e) {
      se !== null && typeof se.markComponentLayoutEffectUnmountStarted == "function" && se.markComponentLayoutEffectUnmountStarted(e);
    }
    function Nd() {
      se !== null && typeof se.markComponentLayoutEffectUnmountStopped == "function" && se.markComponentLayoutEffectUnmountStopped();
    }
    function gs(e, t, a) {
      se !== null && typeof se.markComponentErrored == "function" && se.markComponentErrored(e, t, a);
    }
    function Oi(e, t, a) {
      se !== null && typeof se.markComponentSuspended == "function" && se.markComponentSuspended(e, t, a);
    }
    function Ss(e) {
      se !== null && typeof se.markLayoutEffectsStarted == "function" && se.markLayoutEffectsStarted(e);
    }
    function Es() {
      se !== null && typeof se.markLayoutEffectsStopped == "function" && se.markLayoutEffectsStopped();
    }
    function wu(e) {
      se !== null && typeof se.markPassiveEffectsStarted == "function" && se.markPassiveEffectsStarted(e);
    }
    function Ld() {
      se !== null && typeof se.markPassiveEffectsStopped == "function" && se.markPassiveEffectsStopped();
    }
    function xu(e) {
      se !== null && typeof se.markRenderStarted == "function" && se.markRenderStarted(e);
    }
    function $v() {
      se !== null && typeof se.markRenderYielded == "function" && se.markRenderYielded();
    }
    function Fc() {
      se !== null && typeof se.markRenderStopped == "function" && se.markRenderStopped();
    }
    function Sn(e) {
      se !== null && typeof se.markRenderScheduled == "function" && se.markRenderScheduled(e);
    }
    function Hc(e, t) {
      se !== null && typeof se.markForceUpdateScheduled == "function" && se.markForceUpdateScheduled(e, t);
    }
    function Cs(e, t) {
      se !== null && typeof se.markStateUpdateScheduled == "function" && se.markStateUpdateScheduled(e, t);
    }
    var Ne = (
      /*                         */
      0
    ), ct = (
      /*                 */
      1
    ), Mt = (
      /*                    */
      2
    ), qt = (
      /*               */
      8
    ), Ut = (
      /*              */
      16
    ), An = Math.clz32 ? Math.clz32 : _s, er = Math.log, Vc = Math.LN2;
    function _s(e) {
      var t = e >>> 0;
      return t === 0 ? 32 : 31 - (er(t) / Vc | 0) | 0;
    }
    var ku = 31, Y = (
      /*                        */
      0
    ), Ot = (
      /*                          */
      0
    ), Pe = (
      /*                        */
      1
    ), Vl = (
      /*    */
      2
    ), ui = (
      /*             */
      4
    ), Tr = (
      /*            */
      8
    ), wn = (
      /*                     */
      16
    ), tl = (
      /*                */
      32
    ), Pl = (
      /*                       */
      4194240
    ), Du = (
      /*                        */
      64
    ), Pc = (
      /*                        */
      128
    ), Bc = (
      /*                        */
      256
    ), $c = (
      /*                        */
      512
    ), Ic = (
      /*                        */
      1024
    ), Yc = (
      /*                        */
      2048
    ), Qc = (
      /*                        */
      4096
    ), Wc = (
      /*                        */
      8192
    ), Gc = (
      /*                        */
      16384
    ), Ou = (
      /*                       */
      32768
    ), qc = (
      /*                       */
      65536
    ), To = (
      /*                       */
      131072
    ), bo = (
      /*                       */
      262144
    ), Kc = (
      /*                       */
      524288
    ), Rs = (
      /*                       */
      1048576
    ), Xc = (
      /*                       */
      2097152
    ), Ts = (
      /*                            */
      130023424
    ), Nu = (
      /*                             */
      4194304
    ), Zc = (
      /*                             */
      8388608
    ), bs = (
      /*                             */
      16777216
    ), Jc = (
      /*                             */
      33554432
    ), ef = (
      /*                             */
      67108864
    ), Md = Nu, ws = (
      /*          */
      134217728
    ), Ud = (
      /*                          */
      268435455
    ), xs = (
      /*               */
      268435456
    ), Lu = (
      /*                        */
      536870912
    ), ta = (
      /*                   */
      1073741824
    );
    function Iv(e) {
      {
        if (e & Pe)
          return "Sync";
        if (e & Vl)
          return "InputContinuousHydration";
        if (e & ui)
          return "InputContinuous";
        if (e & Tr)
          return "DefaultHydration";
        if (e & wn)
          return "Default";
        if (e & tl)
          return "TransitionHydration";
        if (e & Pl)
          return "Transition";
        if (e & Ts)
          return "Retry";
        if (e & ws)
          return "SelectiveHydration";
        if (e & xs)
          return "IdleHydration";
        if (e & Lu)
          return "Idle";
        if (e & ta)
          return "Offscreen";
      }
    }
    var Zt = -1, Mu = Du, tf = Nu;
    function ks(e) {
      switch (Bl(e)) {
        case Pe:
          return Pe;
        case Vl:
          return Vl;
        case ui:
          return ui;
        case Tr:
          return Tr;
        case wn:
          return wn;
        case tl:
          return tl;
        case Du:
        case Pc:
        case Bc:
        case $c:
        case Ic:
        case Yc:
        case Qc:
        case Wc:
        case Gc:
        case Ou:
        case qc:
        case To:
        case bo:
        case Kc:
        case Rs:
        case Xc:
          return e & Pl;
        case Nu:
        case Zc:
        case bs:
        case Jc:
        case ef:
          return e & Ts;
        case ws:
          return ws;
        case xs:
          return xs;
        case Lu:
          return Lu;
        case ta:
          return ta;
        default:
          return S("Should have found matching lanes. This is a bug in React."), e;
      }
    }
    function nf(e, t) {
      var a = e.pendingLanes;
      if (a === Y)
        return Y;
      var i = Y, u = e.suspendedLanes, s = e.pingedLanes, f = a & Ud;
      if (f !== Y) {
        var p = f & ~u;
        if (p !== Y)
          i = ks(p);
        else {
          var v = f & s;
          v !== Y && (i = ks(v));
        }
      } else {
        var y = a & ~u;
        y !== Y ? i = ks(y) : s !== Y && (i = ks(s));
      }
      if (i === Y)
        return Y;
      if (t !== Y && t !== i && // If we already suspended with a delay, then interrupting is fine. Don't
      // bother waiting until the root is complete.
      (t & u) === Y) {
        var g = Bl(i), x = Bl(t);
        if (
          // Tests whether the next lane is equal or lower priority than the wip
          // one. This works because the bits decrease in priority as you go left.
          g >= x || // Default priority updates should not interrupt transition updates. The
          // only difference between default updates and transition updates is that
          // default updates do not support refresh transitions.
          g === wn && (x & Pl) !== Y
        )
          return t;
      }
      (i & ui) !== Y && (i |= a & wn);
      var b = e.entangledLanes;
      if (b !== Y)
        for (var U = e.entanglements, F = i & b; F > 0; ) {
          var V = jn(F), ce = 1 << V;
          i |= U[V], F &= ~ce;
        }
      return i;
    }
    function oi(e, t) {
      for (var a = e.eventTimes, i = Zt; t > 0; ) {
        var u = jn(t), s = 1 << u, f = a[u];
        f > i && (i = f), t &= ~s;
      }
      return i;
    }
    function zd(e, t) {
      switch (e) {
        case Pe:
        case Vl:
        case ui:
          return t + 250;
        case Tr:
        case wn:
        case tl:
        case Du:
        case Pc:
        case Bc:
        case $c:
        case Ic:
        case Yc:
        case Qc:
        case Wc:
        case Gc:
        case Ou:
        case qc:
        case To:
        case bo:
        case Kc:
        case Rs:
        case Xc:
          return t + 5e3;
        case Nu:
        case Zc:
        case bs:
        case Jc:
        case ef:
          return Zt;
        case ws:
        case xs:
        case Lu:
        case ta:
          return Zt;
        default:
          return S("Should have found matching lanes. This is a bug in React."), Zt;
      }
    }
    function rf(e, t) {
      for (var a = e.pendingLanes, i = e.suspendedLanes, u = e.pingedLanes, s = e.expirationTimes, f = a; f > 0; ) {
        var p = jn(f), v = 1 << p, y = s[p];
        y === Zt ? ((v & i) === Y || (v & u) !== Y) && (s[p] = zd(v, t)) : y <= t && (e.expiredLanes |= v), f &= ~v;
      }
    }
    function Yv(e) {
      return ks(e.pendingLanes);
    }
    function af(e) {
      var t = e.pendingLanes & ~ta;
      return t !== Y ? t : t & ta ? ta : Y;
    }
    function Qv(e) {
      return (e & Pe) !== Y;
    }
    function Ds(e) {
      return (e & Ud) !== Y;
    }
    function Uu(e) {
      return (e & Ts) === e;
    }
    function Ad(e) {
      var t = Pe | ui | wn;
      return (e & t) === Y;
    }
    function jd(e) {
      return (e & Pl) === e;
    }
    function lf(e, t) {
      var a = Vl | ui | Tr | wn;
      return (t & a) !== Y;
    }
    function Wv(e, t) {
      return (t & e.expiredLanes) !== Y;
    }
    function Fd(e) {
      return (e & Pl) !== Y;
    }
    function Hd() {
      var e = Mu;
      return Mu <<= 1, (Mu & Pl) === Y && (Mu = Du), e;
    }
    function Gv() {
      var e = tf;
      return tf <<= 1, (tf & Ts) === Y && (tf = Nu), e;
    }
    function Bl(e) {
      return e & -e;
    }
    function Os(e) {
      return Bl(e);
    }
    function jn(e) {
      return 31 - An(e);
    }
    function sr(e) {
      return jn(e);
    }
    function na(e, t) {
      return (e & t) !== Y;
    }
    function zu(e, t) {
      return (e & t) === t;
    }
    function et(e, t) {
      return e | t;
    }
    function Ns(e, t) {
      return e & ~t;
    }
    function Vd(e, t) {
      return e & t;
    }
    function qv(e) {
      return e;
    }
    function Kv(e, t) {
      return e !== Ot && e < t ? e : t;
    }
    function Ls(e) {
      for (var t = [], a = 0; a < ku; a++)
        t.push(e);
      return t;
    }
    function wo(e, t, a) {
      e.pendingLanes |= t, t !== Lu && (e.suspendedLanes = Y, e.pingedLanes = Y);
      var i = e.eventTimes, u = sr(t);
      i[u] = a;
    }
    function Xv(e, t) {
      e.suspendedLanes |= t, e.pingedLanes &= ~t;
      for (var a = e.expirationTimes, i = t; i > 0; ) {
        var u = jn(i), s = 1 << u;
        a[u] = Zt, i &= ~s;
      }
    }
    function uf(e, t, a) {
      e.pingedLanes |= e.suspendedLanes & t;
    }
    function Pd(e, t) {
      var a = e.pendingLanes & ~t;
      e.pendingLanes = t, e.suspendedLanes = Y, e.pingedLanes = Y, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t;
      for (var i = e.entanglements, u = e.eventTimes, s = e.expirationTimes, f = a; f > 0; ) {
        var p = jn(f), v = 1 << p;
        i[p] = Y, u[p] = Zt, s[p] = Zt, f &= ~v;
      }
    }
    function of(e, t) {
      for (var a = e.entangledLanes |= t, i = e.entanglements, u = a; u; ) {
        var s = jn(u), f = 1 << s;
        // Is this one of the newly entangled lanes?
        f & t | // Is this lane transitively entangled with the newly entangled lanes?
        i[s] & t && (i[s] |= t), u &= ~f;
      }
    }
    function Bd(e, t) {
      var a = Bl(t), i;
      switch (a) {
        case ui:
          i = Vl;
          break;
        case wn:
          i = Tr;
          break;
        case Du:
        case Pc:
        case Bc:
        case $c:
        case Ic:
        case Yc:
        case Qc:
        case Wc:
        case Gc:
        case Ou:
        case qc:
        case To:
        case bo:
        case Kc:
        case Rs:
        case Xc:
        case Nu:
        case Zc:
        case bs:
        case Jc:
        case ef:
          i = tl;
          break;
        case Lu:
          i = xs;
          break;
        default:
          i = Ot;
          break;
      }
      return (i & (e.suspendedLanes | t)) !== Ot ? Ot : i;
    }
    function Ms(e, t, a) {
      if (ea)
        for (var i = e.pendingUpdatersLaneMap; a > 0; ) {
          var u = sr(a), s = 1 << u, f = i[u];
          f.add(t), a &= ~s;
        }
    }
    function Zv(e, t) {
      if (ea)
        for (var a = e.pendingUpdatersLaneMap, i = e.memoizedUpdaters; t > 0; ) {
          var u = sr(t), s = 1 << u, f = a[u];
          f.size > 0 && (f.forEach(function(p) {
            var v = p.alternate;
            (v === null || !i.has(v)) && i.add(p);
          }), f.clear()), t &= ~s;
        }
    }
    function $d(e, t) {
      return null;
    }
    var Mr = Pe, Ni = ui, ja = wn, Fa = Lu, Us = Ot;
    function Ha() {
      return Us;
    }
    function Fn(e) {
      Us = e;
    }
    function Jv(e, t) {
      var a = Us;
      try {
        return Us = e, t();
      } finally {
        Us = a;
      }
    }
    function eh(e, t) {
      return e !== 0 && e < t ? e : t;
    }
    function zs(e, t) {
      return e > t ? e : t;
    }
    function tr(e, t) {
      return e !== 0 && e < t;
    }
    function th(e) {
      var t = Bl(e);
      return tr(Mr, t) ? tr(Ni, t) ? Ds(t) ? ja : Fa : Ni : Mr;
    }
    function sf(e) {
      var t = e.current.memoizedState;
      return t.isDehydrated;
    }
    var As;
    function br(e) {
      As = e;
    }
    function yy(e) {
      As(e);
    }
    var ye;
    function xo(e) {
      ye = e;
    }
    var cf;
    function nh(e) {
      cf = e;
    }
    var rh;
    function js(e) {
      rh = e;
    }
    var Fs;
    function Id(e) {
      Fs = e;
    }
    var ff = !1, Hs = [], nl = null, Li = null, Mi = null, xn = /* @__PURE__ */ new Map(), Ur = /* @__PURE__ */ new Map(), zr = [], ah = [
      "mousedown",
      "mouseup",
      "touchcancel",
      "touchend",
      "touchstart",
      "auxclick",
      "dblclick",
      "pointercancel",
      "pointerdown",
      "pointerup",
      "dragend",
      "dragstart",
      "drop",
      "compositionend",
      "compositionstart",
      "keydown",
      "keypress",
      "keyup",
      "input",
      "textInput",
      // Intentionally camelCase
      "copy",
      "cut",
      "paste",
      "click",
      "change",
      "contextmenu",
      "reset",
      "submit"
    ];
    function ih(e) {
      return ah.indexOf(e) > -1;
    }
    function si(e, t, a, i, u) {
      return {
        blockedOn: e,
        domEventName: t,
        eventSystemFlags: a,
        nativeEvent: u,
        targetContainers: [i]
      };
    }
    function Yd(e, t) {
      switch (e) {
        case "focusin":
        case "focusout":
          nl = null;
          break;
        case "dragenter":
        case "dragleave":
          Li = null;
          break;
        case "mouseover":
        case "mouseout":
          Mi = null;
          break;
        case "pointerover":
        case "pointerout": {
          var a = t.pointerId;
          xn.delete(a);
          break;
        }
        case "gotpointercapture":
        case "lostpointercapture": {
          var i = t.pointerId;
          Ur.delete(i);
          break;
        }
      }
    }
    function ra(e, t, a, i, u, s) {
      if (e === null || e.nativeEvent !== s) {
        var f = si(t, a, i, u, s);
        if (t !== null) {
          var p = Ao(t);
          p !== null && ye(p);
        }
        return f;
      }
      e.eventSystemFlags |= i;
      var v = e.targetContainers;
      return u !== null && v.indexOf(u) === -1 && v.push(u), e;
    }
    function gy(e, t, a, i, u) {
      switch (t) {
        case "focusin": {
          var s = u;
          return nl = ra(nl, e, t, a, i, s), !0;
        }
        case "dragenter": {
          var f = u;
          return Li = ra(Li, e, t, a, i, f), !0;
        }
        case "mouseover": {
          var p = u;
          return Mi = ra(Mi, e, t, a, i, p), !0;
        }
        case "pointerover": {
          var v = u, y = v.pointerId;
          return xn.set(y, ra(xn.get(y) || null, e, t, a, i, v)), !0;
        }
        case "gotpointercapture": {
          var g = u, x = g.pointerId;
          return Ur.set(x, ra(Ur.get(x) || null, e, t, a, i, g)), !0;
        }
      }
      return !1;
    }
    function Qd(e) {
      var t = Xs(e.target);
      if (t !== null) {
        var a = ha(t);
        if (a !== null) {
          var i = a.tag;
          if (i === De) {
            var u = ki(a);
            if (u !== null) {
              e.blockedOn = u, Fs(e.priority, function() {
                cf(a);
              });
              return;
            }
          } else if (i === te) {
            var s = a.stateNode;
            if (sf(s)) {
              e.blockedOn = Di(a);
              return;
            }
          }
        }
      }
      e.blockedOn = null;
    }
    function lh(e) {
      for (var t = rh(), a = {
        blockedOn: null,
        target: e,
        priority: t
      }, i = 0; i < zr.length && tr(t, zr[i].priority); i++)
        ;
      zr.splice(i, 0, a), i === 0 && Qd(a);
    }
    function Vs(e) {
      if (e.blockedOn !== null)
        return !1;
      for (var t = e.targetContainers; t.length > 0; ) {
        var a = t[0], i = Do(e.domEventName, e.eventSystemFlags, a, e.nativeEvent);
        if (i === null) {
          var u = e.nativeEvent, s = new u.constructor(u.type, u);
          dy(s), u.target.dispatchEvent(s), py();
        } else {
          var f = Ao(i);
          return f !== null && ye(f), e.blockedOn = i, !1;
        }
        t.shift();
      }
      return !0;
    }
    function Wd(e, t, a) {
      Vs(e) && a.delete(t);
    }
    function Sy() {
      ff = !1, nl !== null && Vs(nl) && (nl = null), Li !== null && Vs(Li) && (Li = null), Mi !== null && Vs(Mi) && (Mi = null), xn.forEach(Wd), Ur.forEach(Wd);
    }
    function $l(e, t) {
      e.blockedOn === t && (e.blockedOn = null, ff || (ff = !0, A.unstable_scheduleCallback(A.unstable_NormalPriority, Sy)));
    }
    function Au(e) {
      if (Hs.length > 0) {
        $l(Hs[0], e);
        for (var t = 1; t < Hs.length; t++) {
          var a = Hs[t];
          a.blockedOn === e && (a.blockedOn = null);
        }
      }
      nl !== null && $l(nl, e), Li !== null && $l(Li, e), Mi !== null && $l(Mi, e);
      var i = function(p) {
        return $l(p, e);
      };
      xn.forEach(i), Ur.forEach(i);
      for (var u = 0; u < zr.length; u++) {
        var s = zr[u];
        s.blockedOn === e && (s.blockedOn = null);
      }
      for (; zr.length > 0; ) {
        var f = zr[0];
        if (f.blockedOn !== null)
          break;
        Qd(f), f.blockedOn === null && zr.shift();
      }
    }
    var cr = T.ReactCurrentBatchConfig, _t = !0;
    function qn(e) {
      _t = !!e;
    }
    function Hn() {
      return _t;
    }
    function fr(e, t, a) {
      var i = df(t), u;
      switch (i) {
        case Mr:
          u = Sa;
          break;
        case Ni:
          u = ko;
          break;
        case ja:
        default:
          u = kn;
          break;
      }
      return u.bind(null, t, a, e);
    }
    function Sa(e, t, a, i) {
      var u = Ha(), s = cr.transition;
      cr.transition = null;
      try {
        Fn(Mr), kn(e, t, a, i);
      } finally {
        Fn(u), cr.transition = s;
      }
    }
    function ko(e, t, a, i) {
      var u = Ha(), s = cr.transition;
      cr.transition = null;
      try {
        Fn(Ni), kn(e, t, a, i);
      } finally {
        Fn(u), cr.transition = s;
      }
    }
    function kn(e, t, a, i) {
      _t && Ps(e, t, a, i);
    }
    function Ps(e, t, a, i) {
      var u = Do(e, t, a, i);
      if (u === null) {
        Ay(e, t, i, Ui, a), Yd(e, i);
        return;
      }
      if (gy(u, e, t, a, i)) {
        i.stopPropagation();
        return;
      }
      if (Yd(e, i), t & Na && ih(e)) {
        for (; u !== null; ) {
          var s = Ao(u);
          s !== null && yy(s);
          var f = Do(e, t, a, i);
          if (f === null && Ay(e, t, i, Ui, a), f === u)
            break;
          u = f;
        }
        u !== null && i.stopPropagation();
        return;
      }
      Ay(e, t, i, null, a);
    }
    var Ui = null;
    function Do(e, t, a, i) {
      Ui = null;
      var u = Sd(i), s = Xs(u);
      if (s !== null) {
        var f = ha(s);
        if (f === null)
          s = null;
        else {
          var p = f.tag;
          if (p === De) {
            var v = ki(f);
            if (v !== null)
              return v;
            s = null;
          } else if (p === te) {
            var y = f.stateNode;
            if (sf(y))
              return Di(f);
            s = null;
          } else f !== s && (s = null);
        }
      }
      return Ui = s, null;
    }
    function df(e) {
      switch (e) {
        case "cancel":
        case "click":
        case "close":
        case "contextmenu":
        case "copy":
        case "cut":
        case "auxclick":
        case "dblclick":
        case "dragend":
        case "dragstart":
        case "drop":
        case "focusin":
        case "focusout":
        case "input":
        case "invalid":
        case "keydown":
        case "keypress":
        case "keyup":
        case "mousedown":
        case "mouseup":
        case "paste":
        case "pause":
        case "play":
        case "pointercancel":
        case "pointerdown":
        case "pointerup":
        case "ratechange":
        case "reset":
        case "resize":
        case "seeked":
        case "submit":
        case "touchcancel":
        case "touchend":
        case "touchstart":
        case "volumechange":
        case "change":
        case "selectionchange":
        case "textInput":
        case "compositionstart":
        case "compositionend":
        case "compositionupdate":
        case "beforeblur":
        case "afterblur":
        case "beforeinput":
        case "blur":
        case "fullscreenchange":
        case "focus":
        case "hashchange":
        case "popstate":
        case "select":
        case "selectstart":
          return Mr;
        case "drag":
        case "dragenter":
        case "dragexit":
        case "dragleave":
        case "dragover":
        case "mousemove":
        case "mouseout":
        case "mouseover":
        case "pointermove":
        case "pointerout":
        case "pointerover":
        case "scroll":
        case "toggle":
        case "touchmove":
        case "wheel":
        case "mouseenter":
        case "mouseleave":
        case "pointerenter":
        case "pointerleave":
          return Ni;
        case "message": {
          var t = zc();
          switch (t) {
            case ms:
              return Mr;
            case Fl:
              return Ni;
            case Ji:
            case my:
              return ja;
            case Ru:
              return Fa;
            default:
              return ja;
          }
        }
        default:
          return ja;
      }
    }
    function Bs(e, t, a) {
      return e.addEventListener(t, a, !1), a;
    }
    function aa(e, t, a) {
      return e.addEventListener(t, a, !0), a;
    }
    function Gd(e, t, a, i) {
      return e.addEventListener(t, a, {
        capture: !0,
        passive: i
      }), a;
    }
    function Oo(e, t, a, i) {
      return e.addEventListener(t, a, {
        passive: i
      }), a;
    }
    var Ea = null, No = null, ju = null;
    function Il(e) {
      return Ea = e, No = $s(), !0;
    }
    function pf() {
      Ea = null, No = null, ju = null;
    }
    function rl() {
      if (ju)
        return ju;
      var e, t = No, a = t.length, i, u = $s(), s = u.length;
      for (e = 0; e < a && t[e] === u[e]; e++)
        ;
      var f = a - e;
      for (i = 1; i <= f && t[a - i] === u[s - i]; i++)
        ;
      var p = i > 1 ? 1 - i : void 0;
      return ju = u.slice(e, p), ju;
    }
    function $s() {
      return "value" in Ea ? Ea.value : Ea.textContent;
    }
    function Yl(e) {
      var t, a = e.keyCode;
      return "charCode" in e ? (t = e.charCode, t === 0 && a === 13 && (t = 13)) : t = a, t === 10 && (t = 13), t >= 32 || t === 13 ? t : 0;
    }
    function Lo() {
      return !0;
    }
    function Is() {
      return !1;
    }
    function wr(e) {
      function t(a, i, u, s, f) {
        this._reactName = a, this._targetInst = u, this.type = i, this.nativeEvent = s, this.target = f, this.currentTarget = null;
        for (var p in e)
          if (e.hasOwnProperty(p)) {
            var v = e[p];
            v ? this[p] = v(s) : this[p] = s[p];
          }
        var y = s.defaultPrevented != null ? s.defaultPrevented : s.returnValue === !1;
        return y ? this.isDefaultPrevented = Lo : this.isDefaultPrevented = Is, this.isPropagationStopped = Is, this;
      }
      return nt(t.prototype, {
        preventDefault: function() {
          this.defaultPrevented = !0;
          var a = this.nativeEvent;
          a && (a.preventDefault ? a.preventDefault() : typeof a.returnValue != "unknown" && (a.returnValue = !1), this.isDefaultPrevented = Lo);
        },
        stopPropagation: function() {
          var a = this.nativeEvent;
          a && (a.stopPropagation ? a.stopPropagation() : typeof a.cancelBubble != "unknown" && (a.cancelBubble = !0), this.isPropagationStopped = Lo);
        },
        /**
         * We release all dispatched `SyntheticEvent`s after each event loop, adding
         * them back into the pool. This allows a way to hold onto a reference that
         * won't be added back into the pool.
         */
        persist: function() {
        },
        /**
         * Checks if this event should be released back into the pool.
         *
         * @return {boolean} True if this should not be released, false otherwise.
         */
        isPersistent: Lo
      }), t;
    }
    var Vn = {
      eventPhase: 0,
      bubbles: 0,
      cancelable: 0,
      timeStamp: function(e) {
        return e.timeStamp || Date.now();
      },
      defaultPrevented: 0,
      isTrusted: 0
    }, zi = wr(Vn), Ar = nt({}, Vn, {
      view: 0,
      detail: 0
    }), ia = wr(Ar), vf, Ys, Fu;
    function Ey(e) {
      e !== Fu && (Fu && e.type === "mousemove" ? (vf = e.screenX - Fu.screenX, Ys = e.screenY - Fu.screenY) : (vf = 0, Ys = 0), Fu = e);
    }
    var ci = nt({}, Ar, {
      screenX: 0,
      screenY: 0,
      clientX: 0,
      clientY: 0,
      pageX: 0,
      pageY: 0,
      ctrlKey: 0,
      shiftKey: 0,
      altKey: 0,
      metaKey: 0,
      getModifierState: vn,
      button: 0,
      buttons: 0,
      relatedTarget: function(e) {
        return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
      },
      movementX: function(e) {
        return "movementX" in e ? e.movementX : (Ey(e), vf);
      },
      movementY: function(e) {
        return "movementY" in e ? e.movementY : Ys;
      }
    }), qd = wr(ci), Kd = nt({}, ci, {
      dataTransfer: 0
    }), Hu = wr(Kd), Xd = nt({}, Ar, {
      relatedTarget: 0
    }), al = wr(Xd), uh = nt({}, Vn, {
      animationName: 0,
      elapsedTime: 0,
      pseudoElement: 0
    }), oh = wr(uh), Zd = nt({}, Vn, {
      clipboardData: function(e) {
        return "clipboardData" in e ? e.clipboardData : window.clipboardData;
      }
    }), hf = wr(Zd), Cy = nt({}, Vn, {
      data: 0
    }), sh = wr(Cy), ch = sh, fh = {
      Esc: "Escape",
      Spacebar: " ",
      Left: "ArrowLeft",
      Up: "ArrowUp",
      Right: "ArrowRight",
      Down: "ArrowDown",
      Del: "Delete",
      Win: "OS",
      Menu: "ContextMenu",
      Apps: "ContextMenu",
      Scroll: "ScrollLock",
      MozPrintableKey: "Unidentified"
    }, Vu = {
      8: "Backspace",
      9: "Tab",
      12: "Clear",
      13: "Enter",
      16: "Shift",
      17: "Control",
      18: "Alt",
      19: "Pause",
      20: "CapsLock",
      27: "Escape",
      32: " ",
      33: "PageUp",
      34: "PageDown",
      35: "End",
      36: "Home",
      37: "ArrowLeft",
      38: "ArrowUp",
      39: "ArrowRight",
      40: "ArrowDown",
      45: "Insert",
      46: "Delete",
      112: "F1",
      113: "F2",
      114: "F3",
      115: "F4",
      116: "F5",
      117: "F6",
      118: "F7",
      119: "F8",
      120: "F9",
      121: "F10",
      122: "F11",
      123: "F12",
      144: "NumLock",
      145: "ScrollLock",
      224: "Meta"
    };
    function _y(e) {
      if (e.key) {
        var t = fh[e.key] || e.key;
        if (t !== "Unidentified")
          return t;
      }
      if (e.type === "keypress") {
        var a = Yl(e);
        return a === 13 ? "Enter" : String.fromCharCode(a);
      }
      return e.type === "keydown" || e.type === "keyup" ? Vu[e.keyCode] || "Unidentified" : "";
    }
    var Mo = {
      Alt: "altKey",
      Control: "ctrlKey",
      Meta: "metaKey",
      Shift: "shiftKey"
    };
    function dh(e) {
      var t = this, a = t.nativeEvent;
      if (a.getModifierState)
        return a.getModifierState(e);
      var i = Mo[e];
      return i ? !!a[i] : !1;
    }
    function vn(e) {
      return dh;
    }
    var Ry = nt({}, Ar, {
      key: _y,
      code: 0,
      location: 0,
      ctrlKey: 0,
      shiftKey: 0,
      altKey: 0,
      metaKey: 0,
      repeat: 0,
      locale: 0,
      getModifierState: vn,
      // Legacy Interface
      charCode: function(e) {
        return e.type === "keypress" ? Yl(e) : 0;
      },
      keyCode: function(e) {
        return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
      },
      which: function(e) {
        return e.type === "keypress" ? Yl(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
      }
    }), ph = wr(Ry), Ty = nt({}, ci, {
      pointerId: 0,
      width: 0,
      height: 0,
      pressure: 0,
      tangentialPressure: 0,
      tiltX: 0,
      tiltY: 0,
      twist: 0,
      pointerType: 0,
      isPrimary: 0
    }), vh = wr(Ty), hh = nt({}, Ar, {
      touches: 0,
      targetTouches: 0,
      changedTouches: 0,
      altKey: 0,
      metaKey: 0,
      ctrlKey: 0,
      shiftKey: 0,
      getModifierState: vn
    }), mh = wr(hh), by = nt({}, Vn, {
      propertyName: 0,
      elapsedTime: 0,
      pseudoElement: 0
    }), Va = wr(by), Jd = nt({}, ci, {
      deltaX: function(e) {
        return "deltaX" in e ? e.deltaX : (
          // Fallback to `wheelDeltaX` for Webkit and normalize (right is positive).
          "wheelDeltaX" in e ? -e.wheelDeltaX : 0
        );
      },
      deltaY: function(e) {
        return "deltaY" in e ? e.deltaY : (
          // Fallback to `wheelDeltaY` for Webkit and normalize (down is positive).
          "wheelDeltaY" in e ? -e.wheelDeltaY : (
            // Fallback to `wheelDelta` for IE<9 and normalize (down is positive).
            "wheelDelta" in e ? -e.wheelDelta : 0
          )
        );
      },
      deltaZ: 0,
      // Browsers without "deltaMode" is reporting in raw wheel delta where one
      // notch on the scroll is always +/- 120, roughly equivalent to pixels.
      // A good approximation of DOM_DELTA_LINE (1) is 5% of viewport size or
      // ~40 pixels, for DOM_DELTA_SCREEN (2) it is 87.5% of viewport size.
      deltaMode: 0
    }), wy = wr(Jd), Ql = [9, 13, 27, 32], Qs = 229, il = Nn && "CompositionEvent" in window, Wl = null;
    Nn && "documentMode" in document && (Wl = document.documentMode);
    var ep = Nn && "TextEvent" in window && !Wl, mf = Nn && (!il || Wl && Wl > 8 && Wl <= 11), yh = 32, yf = String.fromCharCode(yh);
    function xy() {
      ot("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]), ot("onCompositionEnd", ["compositionend", "focusout", "keydown", "keypress", "keyup", "mousedown"]), ot("onCompositionStart", ["compositionstart", "focusout", "keydown", "keypress", "keyup", "mousedown"]), ot("onCompositionUpdate", ["compositionupdate", "focusout", "keydown", "keypress", "keyup", "mousedown"]);
    }
    var tp = !1;
    function gh(e) {
      return (e.ctrlKey || e.altKey || e.metaKey) && // ctrlKey && altKey is equivalent to AltGr, and is not a command.
      !(e.ctrlKey && e.altKey);
    }
    function gf(e) {
      switch (e) {
        case "compositionstart":
          return "onCompositionStart";
        case "compositionend":
          return "onCompositionEnd";
        case "compositionupdate":
          return "onCompositionUpdate";
      }
    }
    function Sf(e, t) {
      return e === "keydown" && t.keyCode === Qs;
    }
    function np(e, t) {
      switch (e) {
        case "keyup":
          return Ql.indexOf(t.keyCode) !== -1;
        case "keydown":
          return t.keyCode !== Qs;
        case "keypress":
        case "mousedown":
        case "focusout":
          return !0;
        default:
          return !1;
      }
    }
    function Ef(e) {
      var t = e.detail;
      return typeof t == "object" && "data" in t ? t.data : null;
    }
    function Sh(e) {
      return e.locale === "ko";
    }
    var Pu = !1;
    function rp(e, t, a, i, u) {
      var s, f;
      if (il ? s = gf(t) : Pu ? np(t, i) && (s = "onCompositionEnd") : Sf(t, i) && (s = "onCompositionStart"), !s)
        return null;
      mf && !Sh(i) && (!Pu && s === "onCompositionStart" ? Pu = Il(u) : s === "onCompositionEnd" && Pu && (f = rl()));
      var p = wh(a, s);
      if (p.length > 0) {
        var v = new sh(s, t, null, i, u);
        if (e.push({
          event: v,
          listeners: p
        }), f)
          v.data = f;
        else {
          var y = Ef(i);
          y !== null && (v.data = y);
        }
      }
    }
    function Cf(e, t) {
      switch (e) {
        case "compositionend":
          return Ef(t);
        case "keypress":
          var a = t.which;
          return a !== yh ? null : (tp = !0, yf);
        case "textInput":
          var i = t.data;
          return i === yf && tp ? null : i;
        default:
          return null;
      }
    }
    function ap(e, t) {
      if (Pu) {
        if (e === "compositionend" || !il && np(e, t)) {
          var a = rl();
          return pf(), Pu = !1, a;
        }
        return null;
      }
      switch (e) {
        case "paste":
          return null;
        case "keypress":
          if (!gh(t)) {
            if (t.char && t.char.length > 1)
              return t.char;
            if (t.which)
              return String.fromCharCode(t.which);
          }
          return null;
        case "compositionend":
          return mf && !Sh(t) ? null : t.data;
        default:
          return null;
      }
    }
    function _f(e, t, a, i, u) {
      var s;
      if (ep ? s = Cf(t, i) : s = ap(t, i), !s)
        return null;
      var f = wh(a, "onBeforeInput");
      if (f.length > 0) {
        var p = new ch("onBeforeInput", "beforeinput", null, i, u);
        e.push({
          event: p,
          listeners: f
        }), p.data = s;
      }
    }
    function Eh(e, t, a, i, u, s, f) {
      rp(e, t, a, i, u), _f(e, t, a, i, u);
    }
    var ky = {
      color: !0,
      date: !0,
      datetime: !0,
      "datetime-local": !0,
      email: !0,
      month: !0,
      number: !0,
      password: !0,
      range: !0,
      search: !0,
      tel: !0,
      text: !0,
      time: !0,
      url: !0,
      week: !0
    };
    function Ws(e) {
      var t = e && e.nodeName && e.nodeName.toLowerCase();
      return t === "input" ? !!ky[e.type] : t === "textarea";
    }
    /**
     * Checks if an event is supported in the current execution environment.
     *
     * NOTE: This will not work correctly for non-generic events such as `change`,
     * `reset`, `load`, `error`, and `select`.
     *
     * Borrows from Modernizr.
     *
     * @param {string} eventNameSuffix Event name, e.g. "click".
     * @return {boolean} True if the event is supported.
     * @internal
     * @license Modernizr 3.0.0pre (Custom Build) | MIT
     */
    function Dy(e) {
      if (!Nn)
        return !1;
      var t = "on" + e, a = t in document;
      if (!a) {
        var i = document.createElement("div");
        i.setAttribute(t, "return;"), a = typeof i[t] == "function";
      }
      return a;
    }
    function Gs() {
      ot("onChange", ["change", "click", "focusin", "focusout", "input", "keydown", "keyup", "selectionchange"]);
    }
    function Ch(e, t, a, i) {
      mo(i);
      var u = wh(t, "onChange");
      if (u.length > 0) {
        var s = new zi("onChange", "change", null, a, i);
        e.push({
          event: s,
          listeners: u
        });
      }
    }
    var Gl = null, n = null;
    function r(e) {
      var t = e.nodeName && e.nodeName.toLowerCase();
      return t === "select" || t === "input" && e.type === "file";
    }
    function l(e) {
      var t = [];
      Ch(t, n, e, Sd(e)), Mv(o, t);
    }
    function o(e) {
      jE(e, 0);
    }
    function c(e) {
      var t = kf(e);
      if (_i(t))
        return e;
    }
    function d(e, t) {
      if (e === "change")
        return t;
    }
    var m = !1;
    Nn && (m = Dy("input") && (!document.documentMode || document.documentMode > 9));
    function E(e, t) {
      Gl = e, n = t, Gl.attachEvent("onpropertychange", j);
    }
    function R() {
      Gl && (Gl.detachEvent("onpropertychange", j), Gl = null, n = null);
    }
    function j(e) {
      e.propertyName === "value" && c(n) && l(e);
    }
    function W(e, t, a) {
      e === "focusin" ? (R(), E(t, a)) : e === "focusout" && R();
    }
    function q(e, t) {
      if (e === "selectionchange" || e === "keyup" || e === "keydown")
        return c(n);
    }
    function Q(e) {
      var t = e.nodeName;
      return t && t.toLowerCase() === "input" && (e.type === "checkbox" || e.type === "radio");
    }
    function pe(e, t) {
      if (e === "click")
        return c(t);
    }
    function Se(e, t) {
      if (e === "input" || e === "change")
        return c(t);
    }
    function _e(e) {
      var t = e._wrapperState;
      !t || !t.controlled || e.type !== "number" || Me(e, "number", e.value);
    }
    function Dn(e, t, a, i, u, s, f) {
      var p = a ? kf(a) : window, v, y;
      if (r(p) ? v = d : Ws(p) ? m ? v = Se : (v = q, y = W) : Q(p) && (v = pe), v) {
        var g = v(t, a);
        if (g) {
          Ch(e, g, i, u);
          return;
        }
      }
      y && y(t, p, a), t === "focusout" && _e(p);
    }
    function D() {
      $t("onMouseEnter", ["mouseout", "mouseover"]), $t("onMouseLeave", ["mouseout", "mouseover"]), $t("onPointerEnter", ["pointerout", "pointerover"]), $t("onPointerLeave", ["pointerout", "pointerover"]);
    }
    function w(e, t, a, i, u, s, f) {
      var p = t === "mouseover" || t === "pointerover", v = t === "mouseout" || t === "pointerout";
      if (p && !cs(i)) {
        var y = i.relatedTarget || i.fromElement;
        if (y && (Xs(y) || gp(y)))
          return;
      }
      if (!(!v && !p)) {
        var g;
        if (u.window === u)
          g = u;
        else {
          var x = u.ownerDocument;
          x ? g = x.defaultView || x.parentWindow : g = window;
        }
        var b, U;
        if (v) {
          var F = i.relatedTarget || i.toElement;
          if (b = a, U = F ? Xs(F) : null, U !== null) {
            var V = ha(U);
            (U !== V || U.tag !== fe && U.tag !== qe) && (U = null);
          }
        } else
          b = null, U = a;
        if (b !== U) {
          var ce = qd, Ue = "onMouseLeave", we = "onMouseEnter", Tt = "mouse";
          (t === "pointerout" || t === "pointerover") && (ce = vh, Ue = "onPointerLeave", we = "onPointerEnter", Tt = "pointer");
          var gt = b == null ? g : kf(b), N = U == null ? g : kf(U), P = new ce(Ue, Tt + "leave", b, i, u);
          P.target = gt, P.relatedTarget = N;
          var L = null, K = Xs(u);
          if (K === a) {
            var he = new ce(we, Tt + "enter", U, i, u);
            he.target = N, he.relatedTarget = gt, L = he;
          }
          HR(e, P, L, b, U);
        }
      }
    }
    function M(e, t) {
      return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
    }
    var G = typeof Object.is == "function" ? Object.is : M;
    function Ee(e, t) {
      if (G(e, t))
        return !0;
      if (typeof e != "object" || e === null || typeof t != "object" || t === null)
        return !1;
      var a = Object.keys(e), i = Object.keys(t);
      if (a.length !== i.length)
        return !1;
      for (var u = 0; u < a.length; u++) {
        var s = a[u];
        if (!xr.call(t, s) || !G(e[s], t[s]))
          return !1;
      }
      return !0;
    }
    function ze(e) {
      for (; e && e.firstChild; )
        e = e.firstChild;
      return e;
    }
    function je(e) {
      for (; e; ) {
        if (e.nextSibling)
          return e.nextSibling;
        e = e.parentNode;
      }
    }
    function Ye(e, t) {
      for (var a = ze(e), i = 0, u = 0; a; ) {
        if (a.nodeType === Gi) {
          if (u = i + a.textContent.length, i <= t && u >= t)
            return {
              node: a,
              offset: t - i
            };
          i = u;
        }
        a = ze(je(a));
      }
    }
    function nr(e) {
      var t = e.ownerDocument, a = t && t.defaultView || window, i = a.getSelection && a.getSelection();
      if (!i || i.rangeCount === 0)
        return null;
      var u = i.anchorNode, s = i.anchorOffset, f = i.focusNode, p = i.focusOffset;
      try {
        u.nodeType, f.nodeType;
      } catch {
        return null;
      }
      return zt(e, u, s, f, p);
    }
    function zt(e, t, a, i, u) {
      var s = 0, f = -1, p = -1, v = 0, y = 0, g = e, x = null;
      e: for (; ; ) {
        for (var b = null; g === t && (a === 0 || g.nodeType === Gi) && (f = s + a), g === i && (u === 0 || g.nodeType === Gi) && (p = s + u), g.nodeType === Gi && (s += g.nodeValue.length), (b = g.firstChild) !== null; )
          x = g, g = b;
        for (; ; ) {
          if (g === e)
            break e;
          if (x === t && ++v === a && (f = s), x === i && ++y === u && (p = s), (b = g.nextSibling) !== null)
            break;
          g = x, x = g.parentNode;
        }
        g = b;
      }
      return f === -1 || p === -1 ? null : {
        start: f,
        end: p
      };
    }
    function ql(e, t) {
      var a = e.ownerDocument || document, i = a && a.defaultView || window;
      if (i.getSelection) {
        var u = i.getSelection(), s = e.textContent.length, f = Math.min(t.start, s), p = t.end === void 0 ? f : Math.min(t.end, s);
        if (!u.extend && f > p) {
          var v = p;
          p = f, f = v;
        }
        var y = Ye(e, f), g = Ye(e, p);
        if (y && g) {
          if (u.rangeCount === 1 && u.anchorNode === y.node && u.anchorOffset === y.offset && u.focusNode === g.node && u.focusOffset === g.offset)
            return;
          var x = a.createRange();
          x.setStart(y.node, y.offset), u.removeAllRanges(), f > p ? (u.addRange(x), u.extend(g.node, g.offset)) : (x.setEnd(g.node, g.offset), u.addRange(x));
        }
      }
    }
    function _h(e) {
      return e && e.nodeType === Gi;
    }
    function wE(e, t) {
      return !e || !t ? !1 : e === t ? !0 : _h(e) ? !1 : _h(t) ? wE(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1;
    }
    function CR(e) {
      return e && e.ownerDocument && wE(e.ownerDocument.documentElement, e);
    }
    function _R(e) {
      try {
        return typeof e.contentWindow.location.href == "string";
      } catch {
        return !1;
      }
    }
    function xE() {
      for (var e = window, t = Oa(); t instanceof e.HTMLIFrameElement; ) {
        if (_R(t))
          e = t.contentWindow;
        else
          return t;
        t = Oa(e.document);
      }
      return t;
    }
    function Oy(e) {
      var t = e && e.nodeName && e.nodeName.toLowerCase();
      return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
    }
    function RR() {
      var e = xE();
      return {
        focusedElem: e,
        selectionRange: Oy(e) ? bR(e) : null
      };
    }
    function TR(e) {
      var t = xE(), a = e.focusedElem, i = e.selectionRange;
      if (t !== a && CR(a)) {
        i !== null && Oy(a) && wR(a, i);
        for (var u = [], s = a; s = s.parentNode; )
          s.nodeType === qr && u.push({
            element: s,
            left: s.scrollLeft,
            top: s.scrollTop
          });
        typeof a.focus == "function" && a.focus();
        for (var f = 0; f < u.length; f++) {
          var p = u[f];
          p.element.scrollLeft = p.left, p.element.scrollTop = p.top;
        }
      }
    }
    function bR(e) {
      var t;
      return "selectionStart" in e ? t = {
        start: e.selectionStart,
        end: e.selectionEnd
      } : t = nr(e), t || {
        start: 0,
        end: 0
      };
    }
    function wR(e, t) {
      var a = t.start, i = t.end;
      i === void 0 && (i = a), "selectionStart" in e ? (e.selectionStart = a, e.selectionEnd = Math.min(i, e.value.length)) : ql(e, t);
    }
    var xR = Nn && "documentMode" in document && document.documentMode <= 11;
    function kR() {
      ot("onSelect", ["focusout", "contextmenu", "dragend", "focusin", "keydown", "keyup", "mousedown", "mouseup", "selectionchange"]);
    }
    var Rf = null, Ny = null, ip = null, Ly = !1;
    function DR(e) {
      if ("selectionStart" in e && Oy(e))
        return {
          start: e.selectionStart,
          end: e.selectionEnd
        };
      var t = e.ownerDocument && e.ownerDocument.defaultView || window, a = t.getSelection();
      return {
        anchorNode: a.anchorNode,
        anchorOffset: a.anchorOffset,
        focusNode: a.focusNode,
        focusOffset: a.focusOffset
      };
    }
    function OR(e) {
      return e.window === e ? e.document : e.nodeType === qi ? e : e.ownerDocument;
    }
    function kE(e, t, a) {
      var i = OR(a);
      if (!(Ly || Rf == null || Rf !== Oa(i))) {
        var u = DR(Rf);
        if (!ip || !Ee(ip, u)) {
          ip = u;
          var s = wh(Ny, "onSelect");
          if (s.length > 0) {
            var f = new zi("onSelect", "select", null, t, a);
            e.push({
              event: f,
              listeners: s
            }), f.target = Rf;
          }
        }
      }
    }
    function NR(e, t, a, i, u, s, f) {
      var p = a ? kf(a) : window;
      switch (t) {
        case "focusin":
          (Ws(p) || p.contentEditable === "true") && (Rf = p, Ny = a, ip = null);
          break;
        case "focusout":
          Rf = null, Ny = null, ip = null;
          break;
        case "mousedown":
          Ly = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          Ly = !1, kE(e, i, u);
          break;
        case "selectionchange":
          if (xR)
            break;
        case "keydown":
        case "keyup":
          kE(e, i, u);
      }
    }
    function Rh(e, t) {
      var a = {};
      return a[e.toLowerCase()] = t.toLowerCase(), a["Webkit" + e] = "webkit" + t, a["Moz" + e] = "moz" + t, a;
    }
    var Tf = {
      animationend: Rh("Animation", "AnimationEnd"),
      animationiteration: Rh("Animation", "AnimationIteration"),
      animationstart: Rh("Animation", "AnimationStart"),
      transitionend: Rh("Transition", "TransitionEnd")
    }, My = {}, DE = {};
    Nn && (DE = document.createElement("div").style, "AnimationEvent" in window || (delete Tf.animationend.animation, delete Tf.animationiteration.animation, delete Tf.animationstart.animation), "TransitionEvent" in window || delete Tf.transitionend.transition);
    function Th(e) {
      if (My[e])
        return My[e];
      if (!Tf[e])
        return e;
      var t = Tf[e];
      for (var a in t)
        if (t.hasOwnProperty(a) && a in DE)
          return My[e] = t[a];
      return e;
    }
    var OE = Th("animationend"), NE = Th("animationiteration"), LE = Th("animationstart"), ME = Th("transitionend"), UE = /* @__PURE__ */ new Map(), zE = ["abort", "auxClick", "cancel", "canPlay", "canPlayThrough", "click", "close", "contextMenu", "copy", "cut", "drag", "dragEnd", "dragEnter", "dragExit", "dragLeave", "dragOver", "dragStart", "drop", "durationChange", "emptied", "encrypted", "ended", "error", "gotPointerCapture", "input", "invalid", "keyDown", "keyPress", "keyUp", "load", "loadedData", "loadedMetadata", "loadStart", "lostPointerCapture", "mouseDown", "mouseMove", "mouseOut", "mouseOver", "mouseUp", "paste", "pause", "play", "playing", "pointerCancel", "pointerDown", "pointerMove", "pointerOut", "pointerOver", "pointerUp", "progress", "rateChange", "reset", "resize", "seeked", "seeking", "stalled", "submit", "suspend", "timeUpdate", "touchCancel", "touchEnd", "touchStart", "volumeChange", "scroll", "toggle", "touchMove", "waiting", "wheel"];
    function Uo(e, t) {
      UE.set(e, t), ot(t, [e]);
    }
    function LR() {
      for (var e = 0; e < zE.length; e++) {
        var t = zE[e], a = t.toLowerCase(), i = t[0].toUpperCase() + t.slice(1);
        Uo(a, "on" + i);
      }
      Uo(OE, "onAnimationEnd"), Uo(NE, "onAnimationIteration"), Uo(LE, "onAnimationStart"), Uo("dblclick", "onDoubleClick"), Uo("focusin", "onFocus"), Uo("focusout", "onBlur"), Uo(ME, "onTransitionEnd");
    }
    function MR(e, t, a, i, u, s, f) {
      var p = UE.get(t);
      if (p !== void 0) {
        var v = zi, y = t;
        switch (t) {
          case "keypress":
            if (Yl(i) === 0)
              return;
          case "keydown":
          case "keyup":
            v = ph;
            break;
          case "focusin":
            y = "focus", v = al;
            break;
          case "focusout":
            y = "blur", v = al;
            break;
          case "beforeblur":
          case "afterblur":
            v = al;
            break;
          case "click":
            if (i.button === 2)
              return;
          case "auxclick":
          case "dblclick":
          case "mousedown":
          case "mousemove":
          case "mouseup":
          case "mouseout":
          case "mouseover":
          case "contextmenu":
            v = qd;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = Hu;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = mh;
            break;
          case OE:
          case NE:
          case LE:
            v = oh;
            break;
          case ME:
            v = Va;
            break;
          case "scroll":
            v = ia;
            break;
          case "wheel":
            v = wy;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = hf;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            v = vh;
            break;
        }
        var g = (s & Na) !== 0;
        {
          var x = !g && // TODO: ideally, we'd eventually add all events from
          // nonDelegatedEvents list in DOMPluginEventSystem.
          // Then we can remove this special list.
          // This is a breaking change that can wait until React 18.
          t === "scroll", b = jR(a, p, i.type, g, x);
          if (b.length > 0) {
            var U = new v(p, y, null, i, u);
            e.push({
              event: U,
              listeners: b
            });
          }
        }
      }
    }
    LR(), D(), Gs(), kR(), xy();
    function UR(e, t, a, i, u, s, f) {
      MR(e, t, a, i, u, s);
      var p = (s & gd) === 0;
      p && (w(e, t, a, i, u), Dn(e, t, a, i, u), NR(e, t, a, i, u), Eh(e, t, a, i, u));
    }
    var lp = ["abort", "canplay", "canplaythrough", "durationchange", "emptied", "encrypted", "ended", "error", "loadeddata", "loadedmetadata", "loadstart", "pause", "play", "playing", "progress", "ratechange", "resize", "seeked", "seeking", "stalled", "suspend", "timeupdate", "volumechange", "waiting"], Uy = new Set(["cancel", "close", "invalid", "load", "scroll", "toggle"].concat(lp));
    function AE(e, t, a) {
      var i = e.type || "unknown-event";
      e.currentTarget = a, bi(i, t, void 0, e), e.currentTarget = null;
    }
    function zR(e, t, a) {
      var i;
      if (a)
        for (var u = t.length - 1; u >= 0; u--) {
          var s = t[u], f = s.instance, p = s.currentTarget, v = s.listener;
          if (f !== i && e.isPropagationStopped())
            return;
          AE(e, v, p), i = f;
        }
      else
        for (var y = 0; y < t.length; y++) {
          var g = t[y], x = g.instance, b = g.currentTarget, U = g.listener;
          if (x !== i && e.isPropagationStopped())
            return;
          AE(e, U, b), i = x;
        }
    }
    function jE(e, t) {
      for (var a = (t & Na) !== 0, i = 0; i < e.length; i++) {
        var u = e[i], s = u.event, f = u.listeners;
        zR(s, f, a);
      }
      ps();
    }
    function AR(e, t, a, i, u) {
      var s = Sd(a), f = [];
      UR(f, e, i, a, s, t), jE(f, t);
    }
    function En(e, t) {
      Uy.has(e) || S('Did not expect a listenToNonDelegatedEvent() call for "%s". This is a bug in React. Please file an issue.', e);
      var a = !1, i = db(t), u = VR(e);
      i.has(u) || (FE(t, e, _c, a), i.add(u));
    }
    function zy(e, t, a) {
      Uy.has(e) && !t && S('Did not expect a listenToNativeEvent() call for "%s" in the bubble phase. This is a bug in React. Please file an issue.', e);
      var i = 0;
      t && (i |= Na), FE(a, e, i, t);
    }
    var bh = "_reactListening" + Math.random().toString(36).slice(2);
    function up(e) {
      if (!e[bh]) {
        e[bh] = !0, rt.forEach(function(a) {
          a !== "selectionchange" && (Uy.has(a) || zy(a, !1, e), zy(a, !0, e));
        });
        var t = e.nodeType === qi ? e : e.ownerDocument;
        t !== null && (t[bh] || (t[bh] = !0, zy("selectionchange", !1, t)));
      }
    }
    function FE(e, t, a, i, u) {
      var s = fr(e, t, a), f = void 0;
      ds && (t === "touchstart" || t === "touchmove" || t === "wheel") && (f = !0), e = e, i ? f !== void 0 ? Gd(e, t, s, f) : aa(e, t, s) : f !== void 0 ? Oo(e, t, s, f) : Bs(e, t, s);
    }
    function HE(e, t) {
      return e === t || e.nodeType === Mn && e.parentNode === t;
    }
    function Ay(e, t, a, i, u) {
      var s = i;
      if (!(t & yd) && !(t & _c)) {
        var f = u;
        if (i !== null) {
          var p = i;
          e: for (; ; ) {
            if (p === null)
              return;
            var v = p.tag;
            if (v === te || v === me) {
              var y = p.stateNode.containerInfo;
              if (HE(y, f))
                break;
              if (v === me)
                for (var g = p.return; g !== null; ) {
                  var x = g.tag;
                  if (x === te || x === me) {
                    var b = g.stateNode.containerInfo;
                    if (HE(b, f))
                      return;
                  }
                  g = g.return;
                }
              for (; y !== null; ) {
                var U = Xs(y);
                if (U === null)
                  return;
                var F = U.tag;
                if (F === fe || F === qe) {
                  p = s = U;
                  continue e;
                }
                y = y.parentNode;
              }
            }
            p = p.return;
          }
        }
      }
      Mv(function() {
        return AR(e, t, a, s);
      });
    }
    function op(e, t, a) {
      return {
        instance: e,
        listener: t,
        currentTarget: a
      };
    }
    function jR(e, t, a, i, u, s) {
      for (var f = t !== null ? t + "Capture" : null, p = i ? f : t, v = [], y = e, g = null; y !== null; ) {
        var x = y, b = x.stateNode, U = x.tag;
        if (U === fe && b !== null && (g = b, p !== null)) {
          var F = Ll(y, p);
          F != null && v.push(op(y, F, g));
        }
        if (u)
          break;
        y = y.return;
      }
      return v;
    }
    function wh(e, t) {
      for (var a = t + "Capture", i = [], u = e; u !== null; ) {
        var s = u, f = s.stateNode, p = s.tag;
        if (p === fe && f !== null) {
          var v = f, y = Ll(u, a);
          y != null && i.unshift(op(u, y, v));
          var g = Ll(u, t);
          g != null && i.push(op(u, g, v));
        }
        u = u.return;
      }
      return i;
    }
    function bf(e) {
      if (e === null)
        return null;
      do
        e = e.return;
      while (e && e.tag !== fe);
      return e || null;
    }
    function FR(e, t) {
      for (var a = e, i = t, u = 0, s = a; s; s = bf(s))
        u++;
      for (var f = 0, p = i; p; p = bf(p))
        f++;
      for (; u - f > 0; )
        a = bf(a), u--;
      for (; f - u > 0; )
        i = bf(i), f--;
      for (var v = u; v--; ) {
        if (a === i || i !== null && a === i.alternate)
          return a;
        a = bf(a), i = bf(i);
      }
      return null;
    }
    function VE(e, t, a, i, u) {
      for (var s = t._reactName, f = [], p = a; p !== null && p !== i; ) {
        var v = p, y = v.alternate, g = v.stateNode, x = v.tag;
        if (y !== null && y === i)
          break;
        if (x === fe && g !== null) {
          var b = g;
          if (u) {
            var U = Ll(p, s);
            U != null && f.unshift(op(p, U, b));
          } else if (!u) {
            var F = Ll(p, s);
            F != null && f.push(op(p, F, b));
          }
        }
        p = p.return;
      }
      f.length !== 0 && e.push({
        event: t,
        listeners: f
      });
    }
    function HR(e, t, a, i, u) {
      var s = i && u ? FR(i, u) : null;
      i !== null && VE(e, t, i, s, !1), u !== null && a !== null && VE(e, a, u, s, !0);
    }
    function VR(e, t) {
      return e + "__bubble";
    }
    var Pa = !1, sp = "dangerouslySetInnerHTML", xh = "suppressContentEditableWarning", zo = "suppressHydrationWarning", PE = "autoFocus", qs = "children", Ks = "style", kh = "__html", jy, Dh, cp, BE, Oh, $E, IE;
    jy = {
      // There are working polyfills for <dialog>. Let people use it.
      dialog: !0,
      // Electron ships a custom <webview> tag to display external web content in
      // an isolated frame and process.
      // This tag is not present in non Electron environments such as JSDom which
      // is often used for testing purposes.
      // @see https://electronjs.org/docs/api/webview-tag
      webview: !0
    }, Dh = function(e, t) {
      vd(e, t), Ec(e, t), Ov(e, t, {
        registrationNameDependencies: tt,
        possibleRegistrationNames: at
      });
    }, $E = Nn && !document.documentMode, cp = function(e, t, a) {
      if (!Pa) {
        var i = Nh(a), u = Nh(t);
        u !== i && (Pa = !0, S("Prop `%s` did not match. Server: %s Client: %s", e, JSON.stringify(u), JSON.stringify(i)));
      }
    }, BE = function(e) {
      if (!Pa) {
        Pa = !0;
        var t = [];
        e.forEach(function(a) {
          t.push(a);
        }), S("Extra attributes from the server: %s", t);
      }
    }, Oh = function(e, t) {
      t === !1 ? S("Expected `%s` listener to be a function, instead got `false`.\n\nIf you used to conditionally omit it with %s={condition && value}, pass %s={condition ? value : undefined} instead.", e, e, e) : S("Expected `%s` listener to be a function, instead got a value of `%s` type.", e, typeof t);
    }, IE = function(e, t) {
      var a = e.namespaceURI === Wi ? e.ownerDocument.createElement(e.tagName) : e.ownerDocument.createElementNS(e.namespaceURI, e.tagName);
      return a.innerHTML = t, a.innerHTML;
    };
    var PR = /\r\n?/g, BR = /\u0000|\uFFFD/g;
    function Nh(e) {
      Xn(e);
      var t = typeof e == "string" ? e : "" + e;
      return t.replace(PR, `
`).replace(BR, "");
    }
    function Lh(e, t, a, i) {
      var u = Nh(t), s = Nh(e);
      if (s !== u && (i && (Pa || (Pa = !0, S('Text content did not match. Server: "%s" Client: "%s"', s, u))), a && Re))
        throw new Error("Text content does not match server-rendered HTML.");
    }
    function YE(e) {
      return e.nodeType === qi ? e : e.ownerDocument;
    }
    function $R() {
    }
    function Mh(e) {
      e.onclick = $R;
    }
    function IR(e, t, a, i, u) {
      for (var s in i)
        if (i.hasOwnProperty(s)) {
          var f = i[s];
          if (s === Ks)
            f && Object.freeze(f), Tv(t, f);
          else if (s === sp) {
            var p = f ? f[kh] : void 0;
            p != null && dv(t, p);
          } else if (s === qs)
            if (typeof f == "string") {
              var v = e !== "textarea" || f !== "";
              v && fo(t, f);
            } else typeof f == "number" && fo(t, "" + f);
          else s === xh || s === zo || s === PE || (tt.hasOwnProperty(s) ? f != null && (typeof f != "function" && Oh(s, f), s === "onScroll" && En("scroll", t)) : f != null && kr(t, s, f, u));
        }
    }
    function YR(e, t, a, i) {
      for (var u = 0; u < t.length; u += 2) {
        var s = t[u], f = t[u + 1];
        s === Ks ? Tv(e, f) : s === sp ? dv(e, f) : s === qs ? fo(e, f) : kr(e, s, f, i);
      }
    }
    function QR(e, t, a, i) {
      var u, s = YE(a), f, p = i;
      if (p === Wi && (p = ud(e)), p === Wi) {
        if (u = Ol(e, t), !u && e !== e.toLowerCase() && S("<%s /> is using incorrect casing. Use PascalCase for React components, or lowercase for HTML elements.", e), e === "script") {
          var v = s.createElement("div");
          v.innerHTML = "<script><\/script>";
          var y = v.firstChild;
          f = v.removeChild(y);
        } else if (typeof t.is == "string")
          f = s.createElement(e, {
            is: t.is
          });
        else if (f = s.createElement(e), e === "select") {
          var g = f;
          t.multiple ? g.multiple = !0 : t.size && (g.size = t.size);
        }
      } else
        f = s.createElementNS(p, e);
      return p === Wi && !u && Object.prototype.toString.call(f) === "[object HTMLUnknownElement]" && !xr.call(jy, e) && (jy[e] = !0, S("The tag <%s> is unrecognized in this browser. If you meant to render a React component, start its name with an uppercase letter.", e)), f;
    }
    function WR(e, t) {
      return YE(t).createTextNode(e);
    }
    function GR(e, t, a, i) {
      var u = Ol(t, a);
      Dh(t, a);
      var s;
      switch (t) {
        case "dialog":
          En("cancel", e), En("close", e), s = a;
          break;
        case "iframe":
        case "object":
        case "embed":
          En("load", e), s = a;
          break;
        case "video":
        case "audio":
          for (var f = 0; f < lp.length; f++)
            En(lp[f], e);
          s = a;
          break;
        case "source":
          En("error", e), s = a;
          break;
        case "img":
        case "image":
        case "link":
          En("error", e), En("load", e), s = a;
          break;
        case "details":
          En("toggle", e), s = a;
          break;
        case "input":
          ai(e, a), s = co(e, a), En("invalid", e);
          break;
        case "option":
          xt(e, a), s = a;
          break;
        case "select":
          hu(e, a), s = rs(e, a), En("invalid", e);
          break;
        case "textarea":
          ad(e, a), s = rd(e, a), En("invalid", e);
          break;
        default:
          s = a;
      }
      switch (gc(t, s), IR(t, e, i, s, u), t) {
        case "input":
          ri(e), z(e, a, !1);
          break;
        case "textarea":
          ri(e), cv(e);
          break;
        case "option":
          rn(e, a);
          break;
        case "select":
          td(e, a);
          break;
        default:
          typeof s.onClick == "function" && Mh(e);
          break;
      }
    }
    function qR(e, t, a, i, u) {
      Dh(t, i);
      var s = null, f, p;
      switch (t) {
        case "input":
          f = co(e, a), p = co(e, i), s = [];
          break;
        case "select":
          f = rs(e, a), p = rs(e, i), s = [];
          break;
        case "textarea":
          f = rd(e, a), p = rd(e, i), s = [];
          break;
        default:
          f = a, p = i, typeof f.onClick != "function" && typeof p.onClick == "function" && Mh(e);
          break;
      }
      gc(t, p);
      var v, y, g = null;
      for (v in f)
        if (!(p.hasOwnProperty(v) || !f.hasOwnProperty(v) || f[v] == null))
          if (v === Ks) {
            var x = f[v];
            for (y in x)
              x.hasOwnProperty(y) && (g || (g = {}), g[y] = "");
          } else v === sp || v === qs || v === xh || v === zo || v === PE || (tt.hasOwnProperty(v) ? s || (s = []) : (s = s || []).push(v, null));
      for (v in p) {
        var b = p[v], U = f != null ? f[v] : void 0;
        if (!(!p.hasOwnProperty(v) || b === U || b == null && U == null))
          if (v === Ks)
            if (b && Object.freeze(b), U) {
              for (y in U)
                U.hasOwnProperty(y) && (!b || !b.hasOwnProperty(y)) && (g || (g = {}), g[y] = "");
              for (y in b)
                b.hasOwnProperty(y) && U[y] !== b[y] && (g || (g = {}), g[y] = b[y]);
            } else
              g || (s || (s = []), s.push(v, g)), g = b;
          else if (v === sp) {
            var F = b ? b[kh] : void 0, V = U ? U[kh] : void 0;
            F != null && V !== F && (s = s || []).push(v, F);
          } else v === qs ? (typeof b == "string" || typeof b == "number") && (s = s || []).push(v, "" + b) : v === xh || v === zo || (tt.hasOwnProperty(v) ? (b != null && (typeof b != "function" && Oh(v, b), v === "onScroll" && En("scroll", e)), !s && U !== b && (s = [])) : (s = s || []).push(v, b));
      }
      return g && (cy(g, p[Ks]), (s = s || []).push(Ks, g)), s;
    }
    function KR(e, t, a, i, u) {
      a === "input" && u.type === "radio" && u.name != null && h(e, u);
      var s = Ol(a, i), f = Ol(a, u);
      switch (YR(e, t, s, f), a) {
        case "input":
          C(e, u);
          break;
        case "textarea":
          sv(e, u);
          break;
        case "select":
          hc(e, u);
          break;
      }
    }
    function XR(e) {
      {
        var t = e.toLowerCase();
        return os.hasOwnProperty(t) && os[t] || null;
      }
    }
    function ZR(e, t, a, i, u, s, f) {
      var p, v;
      switch (p = Ol(t, a), Dh(t, a), t) {
        case "dialog":
          En("cancel", e), En("close", e);
          break;
        case "iframe":
        case "object":
        case "embed":
          En("load", e);
          break;
        case "video":
        case "audio":
          for (var y = 0; y < lp.length; y++)
            En(lp[y], e);
          break;
        case "source":
          En("error", e);
          break;
        case "img":
        case "image":
        case "link":
          En("error", e), En("load", e);
          break;
        case "details":
          En("toggle", e);
          break;
        case "input":
          ai(e, a), En("invalid", e);
          break;
        case "option":
          xt(e, a);
          break;
        case "select":
          hu(e, a), En("invalid", e);
          break;
        case "textarea":
          ad(e, a), En("invalid", e);
          break;
      }
      gc(t, a);
      {
        v = /* @__PURE__ */ new Set();
        for (var g = e.attributes, x = 0; x < g.length; x++) {
          var b = g[x].name.toLowerCase();
          switch (b) {
            case "value":
              break;
            case "checked":
              break;
            case "selected":
              break;
            default:
              v.add(g[x].name);
          }
        }
      }
      var U = null;
      for (var F in a)
        if (a.hasOwnProperty(F)) {
          var V = a[F];
          if (F === qs)
            typeof V == "string" ? e.textContent !== V && (a[zo] !== !0 && Lh(e.textContent, V, s, f), U = [qs, V]) : typeof V == "number" && e.textContent !== "" + V && (a[zo] !== !0 && Lh(e.textContent, V, s, f), U = [qs, "" + V]);
          else if (tt.hasOwnProperty(F))
            V != null && (typeof V != "function" && Oh(F, V), F === "onScroll" && En("scroll", e));
          else if (f && // Convince Flow we've calculated it (it's DEV-only in this method.)
          typeof p == "boolean") {
            var ce = void 0, Ue = tn(F);
            if (a[zo] !== !0) {
              if (!(F === xh || F === zo || // Controlled attributes are not validated
              // TODO: Only ignore them on controlled tags.
              F === "value" || F === "checked" || F === "selected")) {
                if (F === sp) {
                  var we = e.innerHTML, Tt = V ? V[kh] : void 0;
                  if (Tt != null) {
                    var gt = IE(e, Tt);
                    gt !== we && cp(F, we, gt);
                  }
                } else if (F === Ks) {
                  if (v.delete(F), $E) {
                    var N = oy(V);
                    ce = e.getAttribute("style"), N !== ce && cp(F, ce, N);
                  }
                } else if (p && !k)
                  v.delete(F.toLowerCase()), ce = ou(e, F, V), V !== ce && cp(F, ce, V);
                else if (!hn(F, Ue, p) && !Zn(F, V, Ue, p)) {
                  var P = !1;
                  if (Ue !== null)
                    v.delete(Ue.attributeName), ce = Cl(e, F, V, Ue);
                  else {
                    var L = i;
                    if (L === Wi && (L = ud(t)), L === Wi)
                      v.delete(F.toLowerCase());
                    else {
                      var K = XR(F);
                      K !== null && K !== F && (P = !0, v.delete(K)), v.delete(F);
                    }
                    ce = ou(e, F, V);
                  }
                  var he = k;
                  !he && V !== ce && !P && cp(F, ce, V);
                }
              }
            }
          }
        }
      switch (f && // $FlowFixMe - Should be inferred as not undefined.
      v.size > 0 && a[zo] !== !0 && BE(v), t) {
        case "input":
          ri(e), z(e, a, !0);
          break;
        case "textarea":
          ri(e), cv(e);
          break;
        case "select":
        case "option":
          break;
        default:
          typeof a.onClick == "function" && Mh(e);
          break;
      }
      return U;
    }
    function JR(e, t, a) {
      var i = e.nodeValue !== t;
      return i;
    }
    function Fy(e, t) {
      {
        if (Pa)
          return;
        Pa = !0, S("Did not expect server HTML to contain a <%s> in <%s>.", t.nodeName.toLowerCase(), e.nodeName.toLowerCase());
      }
    }
    function Hy(e, t) {
      {
        if (Pa)
          return;
        Pa = !0, S('Did not expect server HTML to contain the text node "%s" in <%s>.', t.nodeValue, e.nodeName.toLowerCase());
      }
    }
    function Vy(e, t, a) {
      {
        if (Pa)
          return;
        Pa = !0, S("Expected server HTML to contain a matching <%s> in <%s>.", t, e.nodeName.toLowerCase());
      }
    }
    function Py(e, t) {
      {
        if (t === "" || Pa)
          return;
        Pa = !0, S('Expected server HTML to contain a matching text node for "%s" in <%s>.', t, e.nodeName.toLowerCase());
      }
    }
    function eT(e, t, a) {
      switch (t) {
        case "input":
          H(e, a);
          return;
        case "textarea":
          ay(e, a);
          return;
        case "select":
          nd(e, a);
          return;
      }
    }
    var fp = function() {
    }, dp = function() {
    };
    {
      var tT = ["address", "applet", "area", "article", "aside", "base", "basefont", "bgsound", "blockquote", "body", "br", "button", "caption", "center", "col", "colgroup", "dd", "details", "dir", "div", "dl", "dt", "embed", "fieldset", "figcaption", "figure", "footer", "form", "frame", "frameset", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "iframe", "img", "input", "isindex", "li", "link", "listing", "main", "marquee", "menu", "menuitem", "meta", "nav", "noembed", "noframes", "noscript", "object", "ol", "p", "param", "plaintext", "pre", "script", "section", "select", "source", "style", "summary", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "title", "tr", "track", "ul", "wbr", "xmp"], QE = [
        "applet",
        "caption",
        "html",
        "table",
        "td",
        "th",
        "marquee",
        "object",
        "template",
        // https://html.spec.whatwg.org/multipage/syntax.html#html-integration-point
        // TODO: Distinguish by namespace here -- for <title>, including it here
        // errs on the side of fewer warnings
        "foreignObject",
        "desc",
        "title"
      ], nT = QE.concat(["button"]), rT = ["dd", "dt", "li", "option", "optgroup", "p", "rp", "rt"], WE = {
        current: null,
        formTag: null,
        aTagInScope: null,
        buttonTagInScope: null,
        nobrTagInScope: null,
        pTagInButtonScope: null,
        listItemTagAutoclosing: null,
        dlItemTagAutoclosing: null
      };
      dp = function(e, t) {
        var a = nt({}, e || WE), i = {
          tag: t
        };
        return QE.indexOf(t) !== -1 && (a.aTagInScope = null, a.buttonTagInScope = null, a.nobrTagInScope = null), nT.indexOf(t) !== -1 && (a.pTagInButtonScope = null), tT.indexOf(t) !== -1 && t !== "address" && t !== "div" && t !== "p" && (a.listItemTagAutoclosing = null, a.dlItemTagAutoclosing = null), a.current = i, t === "form" && (a.formTag = i), t === "a" && (a.aTagInScope = i), t === "button" && (a.buttonTagInScope = i), t === "nobr" && (a.nobrTagInScope = i), t === "p" && (a.pTagInButtonScope = i), t === "li" && (a.listItemTagAutoclosing = i), (t === "dd" || t === "dt") && (a.dlItemTagAutoclosing = i), a;
      };
      var aT = function(e, t) {
        switch (t) {
          case "select":
            return e === "option" || e === "optgroup" || e === "#text";
          case "optgroup":
            return e === "option" || e === "#text";
          case "option":
            return e === "#text";
          case "tr":
            return e === "th" || e === "td" || e === "style" || e === "script" || e === "template";
          case "tbody":
          case "thead":
          case "tfoot":
            return e === "tr" || e === "style" || e === "script" || e === "template";
          case "colgroup":
            return e === "col" || e === "template";
          case "table":
            return e === "caption" || e === "colgroup" || e === "tbody" || e === "tfoot" || e === "thead" || e === "style" || e === "script" || e === "template";
          case "head":
            return e === "base" || e === "basefont" || e === "bgsound" || e === "link" || e === "meta" || e === "title" || e === "noscript" || e === "noframes" || e === "style" || e === "script" || e === "template";
          case "html":
            return e === "head" || e === "body" || e === "frameset";
          case "frameset":
            return e === "frame";
          case "#document":
            return e === "html";
        }
        switch (e) {
          case "h1":
          case "h2":
          case "h3":
          case "h4":
          case "h5":
          case "h6":
            return t !== "h1" && t !== "h2" && t !== "h3" && t !== "h4" && t !== "h5" && t !== "h6";
          case "rp":
          case "rt":
            return rT.indexOf(t) === -1;
          case "body":
          case "caption":
          case "col":
          case "colgroup":
          case "frameset":
          case "frame":
          case "head":
          case "html":
          case "tbody":
          case "td":
          case "tfoot":
          case "th":
          case "thead":
          case "tr":
            return t == null;
        }
        return !0;
      }, iT = function(e, t) {
        switch (e) {
          case "address":
          case "article":
          case "aside":
          case "blockquote":
          case "center":
          case "details":
          case "dialog":
          case "dir":
          case "div":
          case "dl":
          case "fieldset":
          case "figcaption":
          case "figure":
          case "footer":
          case "header":
          case "hgroup":
          case "main":
          case "menu":
          case "nav":
          case "ol":
          case "p":
          case "section":
          case "summary":
          case "ul":
          case "pre":
          case "listing":
          case "table":
          case "hr":
          case "xmp":
          case "h1":
          case "h2":
          case "h3":
          case "h4":
          case "h5":
          case "h6":
            return t.pTagInButtonScope;
          case "form":
            return t.formTag || t.pTagInButtonScope;
          case "li":
            return t.listItemTagAutoclosing;
          case "dd":
          case "dt":
            return t.dlItemTagAutoclosing;
          case "button":
            return t.buttonTagInScope;
          case "a":
            return t.aTagInScope;
          case "nobr":
            return t.nobrTagInScope;
        }
        return null;
      }, GE = {};
      fp = function(e, t, a) {
        a = a || WE;
        var i = a.current, u = i && i.tag;
        t != null && (e != null && S("validateDOMNesting: when childText is passed, childTag should be null"), e = "#text");
        var s = aT(e, u) ? null : i, f = s ? null : iT(e, a), p = s || f;
        if (p) {
          var v = p.tag, y = !!s + "|" + e + "|" + v;
          if (!GE[y]) {
            GE[y] = !0;
            var g = e, x = "";
            if (e === "#text" ? /\S/.test(t) ? g = "Text nodes" : (g = "Whitespace text nodes", x = " Make sure you don't have any extra whitespace between tags on each line of your source code.") : g = "<" + e + ">", s) {
              var b = "";
              v === "table" && e === "tr" && (b += " Add a <tbody>, <thead> or <tfoot> to your code to match the DOM tree generated by the browser."), S("validateDOMNesting(...): %s cannot appear as a child of <%s>.%s%s", g, v, x, b);
            } else
              S("validateDOMNesting(...): %s cannot appear as a descendant of <%s>.", g, v);
          }
        }
      };
    }
    var Uh = "suppressHydrationWarning", zh = "$", Ah = "/$", pp = "$?", vp = "$!", lT = "style", By = null, $y = null;
    function uT(e) {
      var t, a, i = e.nodeType;
      switch (i) {
        case qi:
        case sd: {
          t = i === qi ? "#document" : "#fragment";
          var u = e.documentElement;
          a = u ? u.namespaceURI : od(null, "");
          break;
        }
        default: {
          var s = i === Mn ? e.parentNode : e, f = s.namespaceURI || null;
          t = s.tagName, a = od(f, t);
          break;
        }
      }
      {
        var p = t.toLowerCase(), v = dp(null, p);
        return {
          namespace: a,
          ancestorInfo: v
        };
      }
    }
    function oT(e, t, a) {
      {
        var i = e, u = od(i.namespace, t), s = dp(i.ancestorInfo, t);
        return {
          namespace: u,
          ancestorInfo: s
        };
      }
    }
    function UD(e) {
      return e;
    }
    function sT(e) {
      By = Hn(), $y = RR();
      var t = null;
      return qn(!1), t;
    }
    function cT(e) {
      TR($y), qn(By), By = null, $y = null;
    }
    function fT(e, t, a, i, u) {
      var s;
      {
        var f = i;
        if (fp(e, null, f.ancestorInfo), typeof t.children == "string" || typeof t.children == "number") {
          var p = "" + t.children, v = dp(f.ancestorInfo, e);
          fp(null, p, v);
        }
        s = f.namespace;
      }
      var y = QR(e, t, a, s);
      return yp(u, y), Xy(y, t), y;
    }
    function dT(e, t) {
      e.appendChild(t);
    }
    function pT(e, t, a, i, u) {
      switch (GR(e, t, a, i), t) {
        case "button":
        case "input":
        case "select":
        case "textarea":
          return !!a.autoFocus;
        case "img":
          return !0;
        default:
          return !1;
      }
    }
    function vT(e, t, a, i, u, s) {
      {
        var f = s;
        if (typeof i.children != typeof a.children && (typeof i.children == "string" || typeof i.children == "number")) {
          var p = "" + i.children, v = dp(f.ancestorInfo, t);
          fp(null, p, v);
        }
      }
      return qR(e, t, a, i);
    }
    function Iy(e, t) {
      return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
    }
    function hT(e, t, a, i) {
      {
        var u = a;
        fp(null, e, u.ancestorInfo);
      }
      var s = WR(e, t);
      return yp(i, s), s;
    }
    function mT() {
      var e = window.event;
      return e === void 0 ? ja : df(e.type);
    }
    var Yy = typeof setTimeout == "function" ? setTimeout : void 0, yT = typeof clearTimeout == "function" ? clearTimeout : void 0, Qy = -1, qE = typeof Promise == "function" ? Promise : void 0, gT = typeof queueMicrotask == "function" ? queueMicrotask : typeof qE < "u" ? function(e) {
      return qE.resolve(null).then(e).catch(ST);
    } : Yy;
    function ST(e) {
      setTimeout(function() {
        throw e;
      });
    }
    function ET(e, t, a, i) {
      switch (t) {
        case "button":
        case "input":
        case "select":
        case "textarea":
          a.autoFocus && e.focus();
          return;
        case "img": {
          a.src && (e.src = a.src);
          return;
        }
      }
    }
    function CT(e, t, a, i, u, s) {
      KR(e, t, a, i, u), Xy(e, u);
    }
    function KE(e) {
      fo(e, "");
    }
    function _T(e, t, a) {
      e.nodeValue = a;
    }
    function RT(e, t) {
      e.appendChild(t);
    }
    function TT(e, t) {
      var a;
      e.nodeType === Mn ? (a = e.parentNode, a.insertBefore(t, e)) : (a = e, a.appendChild(t));
      var i = e._reactRootContainer;
      i == null && a.onclick === null && Mh(a);
    }
    function bT(e, t, a) {
      e.insertBefore(t, a);
    }
    function wT(e, t, a) {
      e.nodeType === Mn ? e.parentNode.insertBefore(t, a) : e.insertBefore(t, a);
    }
    function xT(e, t) {
      e.removeChild(t);
    }
    function kT(e, t) {
      e.nodeType === Mn ? e.parentNode.removeChild(t) : e.removeChild(t);
    }
    function Wy(e, t) {
      var a = t, i = 0;
      do {
        var u = a.nextSibling;
        if (e.removeChild(a), u && u.nodeType === Mn) {
          var s = u.data;
          if (s === Ah)
            if (i === 0) {
              e.removeChild(u), Au(t);
              return;
            } else
              i--;
          else (s === zh || s === pp || s === vp) && i++;
        }
        a = u;
      } while (a);
      Au(t);
    }
    function DT(e, t) {
      e.nodeType === Mn ? Wy(e.parentNode, t) : e.nodeType === qr && Wy(e, t), Au(e);
    }
    function OT(e) {
      e = e;
      var t = e.style;
      typeof t.setProperty == "function" ? t.setProperty("display", "none", "important") : t.display = "none";
    }
    function NT(e) {
      e.nodeValue = "";
    }
    function LT(e, t) {
      e = e;
      var a = t[lT], i = a != null && a.hasOwnProperty("display") ? a.display : null;
      e.style.display = yc("display", i);
    }
    function MT(e, t) {
      e.nodeValue = t;
    }
    function UT(e) {
      e.nodeType === qr ? e.textContent = "" : e.nodeType === qi && e.documentElement && e.removeChild(e.documentElement);
    }
    function zT(e, t, a) {
      return e.nodeType !== qr || t.toLowerCase() !== e.nodeName.toLowerCase() ? null : e;
    }
    function AT(e, t) {
      return t === "" || e.nodeType !== Gi ? null : e;
    }
    function jT(e) {
      return e.nodeType !== Mn ? null : e;
    }
    function XE(e) {
      return e.data === pp;
    }
    function Gy(e) {
      return e.data === vp;
    }
    function FT(e) {
      var t = e.nextSibling && e.nextSibling.dataset, a, i, u;
      return t && (a = t.dgst, i = t.msg, u = t.stck), {
        message: i,
        digest: a,
        stack: u
      };
    }
    function HT(e, t) {
      e._reactRetry = t;
    }
    function jh(e) {
      for (; e != null; e = e.nextSibling) {
        var t = e.nodeType;
        if (t === qr || t === Gi)
          break;
        if (t === Mn) {
          var a = e.data;
          if (a === zh || a === vp || a === pp)
            break;
          if (a === Ah)
            return null;
        }
      }
      return e;
    }
    function hp(e) {
      return jh(e.nextSibling);
    }
    function VT(e) {
      return jh(e.firstChild);
    }
    function PT(e) {
      return jh(e.firstChild);
    }
    function BT(e) {
      return jh(e.nextSibling);
    }
    function $T(e, t, a, i, u, s, f) {
      yp(s, e), Xy(e, a);
      var p;
      {
        var v = u;
        p = v.namespace;
      }
      var y = (s.mode & ct) !== Ne;
      return ZR(e, t, a, p, i, y, f);
    }
    function IT(e, t, a, i) {
      return yp(a, e), a.mode & ct, JR(e, t);
    }
    function YT(e, t) {
      yp(t, e);
    }
    function QT(e) {
      for (var t = e.nextSibling, a = 0; t; ) {
        if (t.nodeType === Mn) {
          var i = t.data;
          if (i === Ah) {
            if (a === 0)
              return hp(t);
            a--;
          } else (i === zh || i === vp || i === pp) && a++;
        }
        t = t.nextSibling;
      }
      return null;
    }
    function ZE(e) {
      for (var t = e.previousSibling, a = 0; t; ) {
        if (t.nodeType === Mn) {
          var i = t.data;
          if (i === zh || i === vp || i === pp) {
            if (a === 0)
              return t;
            a--;
          } else i === Ah && a++;
        }
        t = t.previousSibling;
      }
      return null;
    }
    function WT(e) {
      Au(e);
    }
    function GT(e) {
      Au(e);
    }
    function qT(e) {
      return e !== "head" && e !== "body";
    }
    function KT(e, t, a, i) {
      var u = !0;
      Lh(t.nodeValue, a, i, u);
    }
    function XT(e, t, a, i, u, s) {
      if (t[Uh] !== !0) {
        var f = !0;
        Lh(i.nodeValue, u, s, f);
      }
    }
    function ZT(e, t) {
      t.nodeType === qr ? Fy(e, t) : t.nodeType === Mn || Hy(e, t);
    }
    function JT(e, t) {
      {
        var a = e.parentNode;
        a !== null && (t.nodeType === qr ? Fy(a, t) : t.nodeType === Mn || Hy(a, t));
      }
    }
    function eb(e, t, a, i, u) {
      (u || t[Uh] !== !0) && (i.nodeType === qr ? Fy(a, i) : i.nodeType === Mn || Hy(a, i));
    }
    function tb(e, t, a) {
      Vy(e, t);
    }
    function nb(e, t) {
      Py(e, t);
    }
    function rb(e, t, a) {
      {
        var i = e.parentNode;
        i !== null && Vy(i, t);
      }
    }
    function ab(e, t) {
      {
        var a = e.parentNode;
        a !== null && Py(a, t);
      }
    }
    function ib(e, t, a, i, u, s) {
      (s || t[Uh] !== !0) && Vy(a, i);
    }
    function lb(e, t, a, i, u) {
      (u || t[Uh] !== !0) && Py(a, i);
    }
    function ub(e) {
      S("An error occurred during hydration. The server HTML was replaced with client content in <%s>.", e.nodeName.toLowerCase());
    }
    function ob(e) {
      up(e);
    }
    var wf = Math.random().toString(36).slice(2), xf = "__reactFiber$" + wf, qy = "__reactProps$" + wf, mp = "__reactContainer$" + wf, Ky = "__reactEvents$" + wf, sb = "__reactListeners$" + wf, cb = "__reactHandles$" + wf;
    function fb(e) {
      delete e[xf], delete e[qy], delete e[Ky], delete e[sb], delete e[cb];
    }
    function yp(e, t) {
      t[xf] = e;
    }
    function Fh(e, t) {
      t[mp] = e;
    }
    function JE(e) {
      e[mp] = null;
    }
    function gp(e) {
      return !!e[mp];
    }
    function Xs(e) {
      var t = e[xf];
      if (t)
        return t;
      for (var a = e.parentNode; a; ) {
        if (t = a[mp] || a[xf], t) {
          var i = t.alternate;
          if (t.child !== null || i !== null && i.child !== null)
            for (var u = ZE(e); u !== null; ) {
              var s = u[xf];
              if (s)
                return s;
              u = ZE(u);
            }
          return t;
        }
        e = a, a = e.parentNode;
      }
      return null;
    }
    function Ao(e) {
      var t = e[xf] || e[mp];
      return t && (t.tag === fe || t.tag === qe || t.tag === De || t.tag === te) ? t : null;
    }
    function kf(e) {
      if (e.tag === fe || e.tag === qe)
        return e.stateNode;
      throw new Error("getNodeFromInstance: Invalid argument.");
    }
    function Hh(e) {
      return e[qy] || null;
    }
    function Xy(e, t) {
      e[qy] = t;
    }
    function db(e) {
      var t = e[Ky];
      return t === void 0 && (t = e[Ky] = /* @__PURE__ */ new Set()), t;
    }
    var eC = {}, tC = T.ReactDebugCurrentFrame;
    function Vh(e) {
      if (e) {
        var t = e._owner, a = Ii(e.type, e._source, t ? t.type : null);
        tC.setExtraStackFrame(a);
      } else
        tC.setExtraStackFrame(null);
    }
    function ll(e, t, a, i, u) {
      {
        var s = Function.call.bind(xr);
        for (var f in e)
          if (s(e, f)) {
            var p = void 0;
            try {
              if (typeof e[f] != "function") {
                var v = Error((i || "React class") + ": " + a + " type `" + f + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof e[f] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                throw v.name = "Invariant Violation", v;
              }
              p = e[f](t, f, i, a, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
            } catch (y) {
              p = y;
            }
            p && !(p instanceof Error) && (Vh(u), S("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", i || "React class", a, f, typeof p), Vh(null)), p instanceof Error && !(p.message in eC) && (eC[p.message] = !0, Vh(u), S("Failed %s type: %s", a, p.message), Vh(null));
          }
      }
    }
    var Zy = [], Ph;
    Ph = [];
    var Bu = -1;
    function jo(e) {
      return {
        current: e
      };
    }
    function la(e, t) {
      if (Bu < 0) {
        S("Unexpected pop.");
        return;
      }
      t !== Ph[Bu] && S("Unexpected Fiber popped."), e.current = Zy[Bu], Zy[Bu] = null, Ph[Bu] = null, Bu--;
    }
    function ua(e, t, a) {
      Bu++, Zy[Bu] = e.current, Ph[Bu] = a, e.current = t;
    }
    var Jy;
    Jy = {};
    var fi = {};
    Object.freeze(fi);
    var $u = jo(fi), Kl = jo(!1), eg = fi;
    function Df(e, t, a) {
      return a && Xl(t) ? eg : $u.current;
    }
    function nC(e, t, a) {
      {
        var i = e.stateNode;
        i.__reactInternalMemoizedUnmaskedChildContext = t, i.__reactInternalMemoizedMaskedChildContext = a;
      }
    }
    function Of(e, t) {
      {
        var a = e.type, i = a.contextTypes;
        if (!i)
          return fi;
        var u = e.stateNode;
        if (u && u.__reactInternalMemoizedUnmaskedChildContext === t)
          return u.__reactInternalMemoizedMaskedChildContext;
        var s = {};
        for (var f in i)
          s[f] = t[f];
        {
          var p = Qe(e) || "Unknown";
          ll(i, s, "context", p);
        }
        return u && nC(e, t, s), s;
      }
    }
    function Bh() {
      return Kl.current;
    }
    function Xl(e) {
      {
        var t = e.childContextTypes;
        return t != null;
      }
    }
    function $h(e) {
      la(Kl, e), la($u, e);
    }
    function tg(e) {
      la(Kl, e), la($u, e);
    }
    function rC(e, t, a) {
      {
        if ($u.current !== fi)
          throw new Error("Unexpected context found on stack. This error is likely caused by a bug in React. Please file an issue.");
        ua($u, t, e), ua(Kl, a, e);
      }
    }
    function aC(e, t, a) {
      {
        var i = e.stateNode, u = t.childContextTypes;
        if (typeof i.getChildContext != "function") {
          {
            var s = Qe(e) || "Unknown";
            Jy[s] || (Jy[s] = !0, S("%s.childContextTypes is specified but there is no getChildContext() method on the instance. You can either define getChildContext() on %s or remove childContextTypes from it.", s, s));
          }
          return a;
        }
        var f = i.getChildContext();
        for (var p in f)
          if (!(p in u))
            throw new Error((Qe(e) || "Unknown") + '.getChildContext(): key "' + p + '" is not defined in childContextTypes.');
        {
          var v = Qe(e) || "Unknown";
          ll(u, f, "child context", v);
        }
        return nt({}, a, f);
      }
    }
    function Ih(e) {
      {
        var t = e.stateNode, a = t && t.__reactInternalMemoizedMergedChildContext || fi;
        return eg = $u.current, ua($u, a, e), ua(Kl, Kl.current, e), !0;
      }
    }
    function iC(e, t, a) {
      {
        var i = e.stateNode;
        if (!i)
          throw new Error("Expected to have an instance by this point. This error is likely caused by a bug in React. Please file an issue.");
        if (a) {
          var u = aC(e, t, eg);
          i.__reactInternalMemoizedMergedChildContext = u, la(Kl, e), la($u, e), ua($u, u, e), ua(Kl, a, e);
        } else
          la(Kl, e), ua(Kl, a, e);
      }
    }
    function pb(e) {
      {
        if (!_u(e) || e.tag !== ne)
          throw new Error("Expected subtree parent to be a mounted class component. This error is likely caused by a bug in React. Please file an issue.");
        var t = e;
        do {
          switch (t.tag) {
            case te:
              return t.stateNode.context;
            case ne: {
              var a = t.type;
              if (Xl(a))
                return t.stateNode.__reactInternalMemoizedMergedChildContext;
              break;
            }
          }
          t = t.return;
        } while (t !== null);
        throw new Error("Found unexpected detached subtree parent. This error is likely caused by a bug in React. Please file an issue.");
      }
    }
    var Fo = 0, Yh = 1, Iu = null, ng = !1, rg = !1;
    function lC(e) {
      Iu === null ? Iu = [e] : Iu.push(e);
    }
    function vb(e) {
      ng = !0, lC(e);
    }
    function uC() {
      ng && Ho();
    }
    function Ho() {
      if (!rg && Iu !== null) {
        rg = !0;
        var e = 0, t = Ha();
        try {
          var a = !0, i = Iu;
          for (Fn(Mr); e < i.length; e++) {
            var u = i[e];
            do
              u = u(a);
            while (u !== null);
          }
          Iu = null, ng = !1;
        } catch (s) {
          throw Iu !== null && (Iu = Iu.slice(e + 1)), Cd(ms, Ho), s;
        } finally {
          Fn(t), rg = !1;
        }
      }
      return null;
    }
    var Nf = [], Lf = 0, Qh = null, Wh = 0, Ai = [], ji = 0, Zs = null, Yu = 1, Qu = "";
    function hb(e) {
      return ec(), (e.flags & wi) !== Oe;
    }
    function mb(e) {
      return ec(), Wh;
    }
    function yb() {
      var e = Qu, t = Yu, a = t & ~gb(t);
      return a.toString(32) + e;
    }
    function Js(e, t) {
      ec(), Nf[Lf++] = Wh, Nf[Lf++] = Qh, Qh = e, Wh = t;
    }
    function oC(e, t, a) {
      ec(), Ai[ji++] = Yu, Ai[ji++] = Qu, Ai[ji++] = Zs, Zs = e;
      var i = Yu, u = Qu, s = Gh(i) - 1, f = i & ~(1 << s), p = a + 1, v = Gh(t) + s;
      if (v > 30) {
        var y = s - s % 5, g = (1 << y) - 1, x = (f & g).toString(32), b = f >> y, U = s - y, F = Gh(t) + U, V = p << U, ce = V | b, Ue = x + u;
        Yu = 1 << F | ce, Qu = Ue;
      } else {
        var we = p << s, Tt = we | f, gt = u;
        Yu = 1 << v | Tt, Qu = gt;
      }
    }
    function ag(e) {
      ec();
      var t = e.return;
      if (t !== null) {
        var a = 1, i = 0;
        Js(e, a), oC(e, a, i);
      }
    }
    function Gh(e) {
      return 32 - An(e);
    }
    function gb(e) {
      return 1 << Gh(e) - 1;
    }
    function ig(e) {
      for (; e === Qh; )
        Qh = Nf[--Lf], Nf[Lf] = null, Wh = Nf[--Lf], Nf[Lf] = null;
      for (; e === Zs; )
        Zs = Ai[--ji], Ai[ji] = null, Qu = Ai[--ji], Ai[ji] = null, Yu = Ai[--ji], Ai[ji] = null;
    }
    function Sb() {
      return ec(), Zs !== null ? {
        id: Yu,
        overflow: Qu
      } : null;
    }
    function Eb(e, t) {
      ec(), Ai[ji++] = Yu, Ai[ji++] = Qu, Ai[ji++] = Zs, Yu = t.id, Qu = t.overflow, Zs = e;
    }
    function ec() {
      Fr() || S("Expected to be hydrating. This is a bug in React. Please file an issue.");
    }
    var jr = null, Fi = null, ul = !1, tc = !1, Vo = null;
    function Cb() {
      ul && S("We should not be hydrating here. This is a bug in React. Please file a bug.");
    }
    function sC() {
      tc = !0;
    }
    function _b() {
      return tc;
    }
    function Rb(e) {
      var t = e.stateNode.containerInfo;
      return Fi = PT(t), jr = e, ul = !0, Vo = null, tc = !1, !0;
    }
    function Tb(e, t, a) {
      return Fi = BT(t), jr = e, ul = !0, Vo = null, tc = !1, a !== null && Eb(e, a), !0;
    }
    function cC(e, t) {
      switch (e.tag) {
        case te: {
          ZT(e.stateNode.containerInfo, t);
          break;
        }
        case fe: {
          var a = (e.mode & ct) !== Ne;
          eb(
            e.type,
            e.memoizedProps,
            e.stateNode,
            t,
            // TODO: Delete this argument when we remove the legacy root API.
            a
          );
          break;
        }
        case De: {
          var i = e.memoizedState;
          i.dehydrated !== null && JT(i.dehydrated, t);
          break;
        }
      }
    }
    function fC(e, t) {
      cC(e, t);
      var a = kx();
      a.stateNode = t, a.return = e;
      var i = e.deletions;
      i === null ? (e.deletions = [a], e.flags |= La) : i.push(a);
    }
    function lg(e, t) {
      {
        if (tc)
          return;
        switch (e.tag) {
          case te: {
            var a = e.stateNode.containerInfo;
            switch (t.tag) {
              case fe:
                var i = t.type;
                t.pendingProps, tb(a, i);
                break;
              case qe:
                var u = t.pendingProps;
                nb(a, u);
                break;
            }
            break;
          }
          case fe: {
            var s = e.type, f = e.memoizedProps, p = e.stateNode;
            switch (t.tag) {
              case fe: {
                var v = t.type, y = t.pendingProps, g = (e.mode & ct) !== Ne;
                ib(
                  s,
                  f,
                  p,
                  v,
                  y,
                  // TODO: Delete this argument when we remove the legacy root API.
                  g
                );
                break;
              }
              case qe: {
                var x = t.pendingProps, b = (e.mode & ct) !== Ne;
                lb(
                  s,
                  f,
                  p,
                  x,
                  // TODO: Delete this argument when we remove the legacy root API.
                  b
                );
                break;
              }
            }
            break;
          }
          case De: {
            var U = e.memoizedState, F = U.dehydrated;
            if (F !== null) switch (t.tag) {
              case fe:
                var V = t.type;
                t.pendingProps, rb(F, V);
                break;
              case qe:
                var ce = t.pendingProps;
                ab(F, ce);
                break;
            }
            break;
          }
          default:
            return;
        }
      }
    }
    function dC(e, t) {
      t.flags = t.flags & ~Xr | yn, lg(e, t);
    }
    function pC(e, t) {
      switch (e.tag) {
        case fe: {
          var a = e.type;
          e.pendingProps;
          var i = zT(t, a);
          return i !== null ? (e.stateNode = i, jr = e, Fi = VT(i), !0) : !1;
        }
        case qe: {
          var u = e.pendingProps, s = AT(t, u);
          return s !== null ? (e.stateNode = s, jr = e, Fi = null, !0) : !1;
        }
        case De: {
          var f = jT(t);
          if (f !== null) {
            var p = {
              dehydrated: f,
              treeContext: Sb(),
              retryLane: ta
            };
            e.memoizedState = p;
            var v = Dx(f);
            return v.return = e, e.child = v, jr = e, Fi = null, !0;
          }
          return !1;
        }
        default:
          return !1;
      }
    }
    function ug(e) {
      return (e.mode & ct) !== Ne && (e.flags & xe) === Oe;
    }
    function og(e) {
      throw new Error("Hydration failed because the initial UI does not match what was rendered on the server.");
    }
    function sg(e) {
      if (ul) {
        var t = Fi;
        if (!t) {
          ug(e) && (lg(jr, e), og()), dC(jr, e), ul = !1, jr = e;
          return;
        }
        var a = t;
        if (!pC(e, t)) {
          ug(e) && (lg(jr, e), og()), t = hp(a);
          var i = jr;
          if (!t || !pC(e, t)) {
            dC(jr, e), ul = !1, jr = e;
            return;
          }
          fC(i, a);
        }
      }
    }
    function bb(e, t, a) {
      var i = e.stateNode, u = !tc, s = $T(i, e.type, e.memoizedProps, t, a, e, u);
      return e.updateQueue = s, s !== null;
    }
    function wb(e) {
      var t = e.stateNode, a = e.memoizedProps, i = IT(t, a, e);
      if (i) {
        var u = jr;
        if (u !== null)
          switch (u.tag) {
            case te: {
              var s = u.stateNode.containerInfo, f = (u.mode & ct) !== Ne;
              KT(
                s,
                t,
                a,
                // TODO: Delete this argument when we remove the legacy root API.
                f
              );
              break;
            }
            case fe: {
              var p = u.type, v = u.memoizedProps, y = u.stateNode, g = (u.mode & ct) !== Ne;
              XT(
                p,
                v,
                y,
                t,
                a,
                // TODO: Delete this argument when we remove the legacy root API.
                g
              );
              break;
            }
          }
      }
      return i;
    }
    function xb(e) {
      var t = e.memoizedState, a = t !== null ? t.dehydrated : null;
      if (!a)
        throw new Error("Expected to have a hydrated suspense instance. This error is likely caused by a bug in React. Please file an issue.");
      YT(a, e);
    }
    function kb(e) {
      var t = e.memoizedState, a = t !== null ? t.dehydrated : null;
      if (!a)
        throw new Error("Expected to have a hydrated suspense instance. This error is likely caused by a bug in React. Please file an issue.");
      return QT(a);
    }
    function vC(e) {
      for (var t = e.return; t !== null && t.tag !== fe && t.tag !== te && t.tag !== De; )
        t = t.return;
      jr = t;
    }
    function qh(e) {
      if (e !== jr)
        return !1;
      if (!ul)
        return vC(e), ul = !0, !1;
      if (e.tag !== te && (e.tag !== fe || qT(e.type) && !Iy(e.type, e.memoizedProps))) {
        var t = Fi;
        if (t)
          if (ug(e))
            hC(e), og();
          else
            for (; t; )
              fC(e, t), t = hp(t);
      }
      return vC(e), e.tag === De ? Fi = kb(e) : Fi = jr ? hp(e.stateNode) : null, !0;
    }
    function Db() {
      return ul && Fi !== null;
    }
    function hC(e) {
      for (var t = Fi; t; )
        cC(e, t), t = hp(t);
    }
    function Mf() {
      jr = null, Fi = null, ul = !1, tc = !1;
    }
    function mC() {
      Vo !== null && (s_(Vo), Vo = null);
    }
    function Fr() {
      return ul;
    }
    function cg(e) {
      Vo === null ? Vo = [e] : Vo.push(e);
    }
    var Ob = T.ReactCurrentBatchConfig, Nb = null;
    function Lb() {
      return Ob.transition;
    }
    var ol = {
      recordUnsafeLifecycleWarnings: function(e, t) {
      },
      flushPendingUnsafeLifecycleWarnings: function() {
      },
      recordLegacyContextWarning: function(e, t) {
      },
      flushLegacyContextWarning: function() {
      },
      discardPendingWarnings: function() {
      }
    };
    {
      var Mb = function(e) {
        for (var t = null, a = e; a !== null; )
          a.mode & qt && (t = a), a = a.return;
        return t;
      }, nc = function(e) {
        var t = [];
        return e.forEach(function(a) {
          t.push(a);
        }), t.sort().join(", ");
      }, Sp = [], Ep = [], Cp = [], _p = [], Rp = [], Tp = [], rc = /* @__PURE__ */ new Set();
      ol.recordUnsafeLifecycleWarnings = function(e, t) {
        rc.has(e.type) || (typeof t.componentWillMount == "function" && // Don't warn about react-lifecycles-compat polyfilled components.
        t.componentWillMount.__suppressDeprecationWarning !== !0 && Sp.push(e), e.mode & qt && typeof t.UNSAFE_componentWillMount == "function" && Ep.push(e), typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps.__suppressDeprecationWarning !== !0 && Cp.push(e), e.mode & qt && typeof t.UNSAFE_componentWillReceiveProps == "function" && _p.push(e), typeof t.componentWillUpdate == "function" && t.componentWillUpdate.__suppressDeprecationWarning !== !0 && Rp.push(e), e.mode & qt && typeof t.UNSAFE_componentWillUpdate == "function" && Tp.push(e));
      }, ol.flushPendingUnsafeLifecycleWarnings = function() {
        var e = /* @__PURE__ */ new Set();
        Sp.length > 0 && (Sp.forEach(function(b) {
          e.add(Qe(b) || "Component"), rc.add(b.type);
        }), Sp = []);
        var t = /* @__PURE__ */ new Set();
        Ep.length > 0 && (Ep.forEach(function(b) {
          t.add(Qe(b) || "Component"), rc.add(b.type);
        }), Ep = []);
        var a = /* @__PURE__ */ new Set();
        Cp.length > 0 && (Cp.forEach(function(b) {
          a.add(Qe(b) || "Component"), rc.add(b.type);
        }), Cp = []);
        var i = /* @__PURE__ */ new Set();
        _p.length > 0 && (_p.forEach(function(b) {
          i.add(Qe(b) || "Component"), rc.add(b.type);
        }), _p = []);
        var u = /* @__PURE__ */ new Set();
        Rp.length > 0 && (Rp.forEach(function(b) {
          u.add(Qe(b) || "Component"), rc.add(b.type);
        }), Rp = []);
        var s = /* @__PURE__ */ new Set();
        if (Tp.length > 0 && (Tp.forEach(function(b) {
          s.add(Qe(b) || "Component"), rc.add(b.type);
        }), Tp = []), t.size > 0) {
          var f = nc(t);
          S(`Using UNSAFE_componentWillMount in strict mode is not recommended and may indicate bugs in your code. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move code with side effects to componentDidMount, and set initial state in the constructor.

Please update the following components: %s`, f);
        }
        if (i.size > 0) {
          var p = nc(i);
          S(`Using UNSAFE_componentWillReceiveProps in strict mode is not recommended and may indicate bugs in your code. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* If you're updating state whenever props change, refactor your code to use memoization techniques or move it to static getDerivedStateFromProps. Learn more at: https://reactjs.org/link/derived-state

Please update the following components: %s`, p);
        }
        if (s.size > 0) {
          var v = nc(s);
          S(`Using UNSAFE_componentWillUpdate in strict mode is not recommended and may indicate bugs in your code. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.

Please update the following components: %s`, v);
        }
        if (e.size > 0) {
          var y = nc(e);
          He(`componentWillMount has been renamed, and is not recommended for use. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move code with side effects to componentDidMount, and set initial state in the constructor.
* Rename componentWillMount to UNSAFE_componentWillMount to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`, y);
        }
        if (a.size > 0) {
          var g = nc(a);
          He(`componentWillReceiveProps has been renamed, and is not recommended for use. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* If you're updating state whenever props change, refactor your code to use memoization techniques or move it to static getDerivedStateFromProps. Learn more at: https://reactjs.org/link/derived-state
* Rename componentWillReceiveProps to UNSAFE_componentWillReceiveProps to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`, g);
        }
        if (u.size > 0) {
          var x = nc(u);
          He(`componentWillUpdate has been renamed, and is not recommended for use. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* Rename componentWillUpdate to UNSAFE_componentWillUpdate to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`, x);
        }
      };
      var Kh = /* @__PURE__ */ new Map(), yC = /* @__PURE__ */ new Set();
      ol.recordLegacyContextWarning = function(e, t) {
        var a = Mb(e);
        if (a === null) {
          S("Expected to find a StrictMode component in a strict mode tree. This error is likely caused by a bug in React. Please file an issue.");
          return;
        }
        if (!yC.has(e.type)) {
          var i = Kh.get(a);
          (e.type.contextTypes != null || e.type.childContextTypes != null || t !== null && typeof t.getChildContext == "function") && (i === void 0 && (i = [], Kh.set(a, i)), i.push(e));
        }
      }, ol.flushLegacyContextWarning = function() {
        Kh.forEach(function(e, t) {
          if (e.length !== 0) {
            var a = e[0], i = /* @__PURE__ */ new Set();
            e.forEach(function(s) {
              i.add(Qe(s) || "Component"), yC.add(s.type);
            });
            var u = nc(i);
            try {
              Qt(a), S(`Legacy context API has been detected within a strict-mode tree.

The old API will be supported in all 16.x releases, but applications using it should migrate to the new version.

Please update the following components: %s

Learn more about this warning here: https://reactjs.org/link/legacy-context`, u);
            } finally {
              cn();
            }
          }
        });
      }, ol.discardPendingWarnings = function() {
        Sp = [], Ep = [], Cp = [], _p = [], Rp = [], Tp = [], Kh = /* @__PURE__ */ new Map();
      };
    }
    var fg, dg, pg, vg, hg, gC = function(e, t) {
    };
    fg = !1, dg = !1, pg = {}, vg = {}, hg = {}, gC = function(e, t) {
      if (!(e === null || typeof e != "object") && !(!e._store || e._store.validated || e.key != null)) {
        if (typeof e._store != "object")
          throw new Error("React Component in warnForMissingKey should have a _store. This error is likely caused by a bug in React. Please file an issue.");
        e._store.validated = !0;
        var a = Qe(t) || "Component";
        vg[a] || (vg[a] = !0, S('Each child in a list should have a unique "key" prop. See https://reactjs.org/link/warning-keys for more information.'));
      }
    };
    function Ub(e) {
      return e.prototype && e.prototype.isReactComponent;
    }
    function bp(e, t, a) {
      var i = a.ref;
      if (i !== null && typeof i != "function" && typeof i != "object") {
        if ((e.mode & qt || B) && // We warn in ReactElement.js if owner and self are equal for string refs
        // because these cannot be automatically converted to an arrow function
        // using a codemod. Therefore, we don't have to warn about string refs again.
        !(a._owner && a._self && a._owner.stateNode !== a._self) && // Will already throw with "Function components cannot have string refs"
        !(a._owner && a._owner.tag !== ne) && // Will already warn with "Function components cannot be given refs"
        !(typeof a.type == "function" && !Ub(a.type)) && // Will already throw with "Element ref was specified as a string (someStringRef) but no owner was set"
        a._owner) {
          var u = Qe(e) || "Component";
          pg[u] || (S('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. We recommend using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', u, i), pg[u] = !0);
        }
        if (a._owner) {
          var s = a._owner, f;
          if (s) {
            var p = s;
            if (p.tag !== ne)
              throw new Error("Function components cannot have string refs. We recommend using useRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref");
            f = p.stateNode;
          }
          if (!f)
            throw new Error("Missing owner for string ref " + i + ". This error is likely caused by a bug in React. Please file an issue.");
          var v = f;
          vi(i, "ref");
          var y = "" + i;
          if (t !== null && t.ref !== null && typeof t.ref == "function" && t.ref._stringRef === y)
            return t.ref;
          var g = function(x) {
            var b = v.refs;
            x === null ? delete b[y] : b[y] = x;
          };
          return g._stringRef = y, g;
        } else {
          if (typeof i != "string")
            throw new Error("Expected ref to be a function, a string, an object returned by React.createRef(), or null.");
          if (!a._owner)
            throw new Error("Element ref was specified as a string (" + i + `) but no owner was set. This could happen for one of the following reasons:
1. You may be adding a ref to a function component
2. You may be adding a ref to a component that was not created inside a component's render method
3. You have multiple copies of React loaded
See https://reactjs.org/link/refs-must-have-owner for more information.`);
        }
      }
      return i;
    }
    function Xh(e, t) {
      var a = Object.prototype.toString.call(t);
      throw new Error("Objects are not valid as a React child (found: " + (a === "[object Object]" ? "object with keys {" + Object.keys(t).join(", ") + "}" : a) + "). If you meant to render a collection of children, use an array instead.");
    }
    function Zh(e) {
      {
        var t = Qe(e) || "Component";
        if (hg[t])
          return;
        hg[t] = !0, S("Functions are not valid as a React child. This may happen if you return a Component instead of <Component /> from render. Or maybe you meant to call this function rather than return it.");
      }
    }
    function SC(e) {
      var t = e._payload, a = e._init;
      return a(t);
    }
    function EC(e) {
      function t(N, P) {
        if (e) {
          var L = N.deletions;
          L === null ? (N.deletions = [P], N.flags |= La) : L.push(P);
        }
      }
      function a(N, P) {
        if (!e)
          return null;
        for (var L = P; L !== null; )
          t(N, L), L = L.sibling;
        return null;
      }
      function i(N, P) {
        for (var L = /* @__PURE__ */ new Map(), K = P; K !== null; )
          K.key !== null ? L.set(K.key, K) : L.set(K.index, K), K = K.sibling;
        return L;
      }
      function u(N, P) {
        var L = dc(N, P);
        return L.index = 0, L.sibling = null, L;
      }
      function s(N, P, L) {
        if (N.index = L, !e)
          return N.flags |= wi, P;
        var K = N.alternate;
        if (K !== null) {
          var he = K.index;
          return he < P ? (N.flags |= yn, P) : he;
        } else
          return N.flags |= yn, P;
      }
      function f(N) {
        return e && N.alternate === null && (N.flags |= yn), N;
      }
      function p(N, P, L, K) {
        if (P === null || P.tag !== qe) {
          var he = cE(L, N.mode, K);
          return he.return = N, he;
        } else {
          var de = u(P, L);
          return de.return = N, de;
        }
      }
      function v(N, P, L, K) {
        var he = L.type;
        if (he === mi)
          return g(N, P, L.props.children, K, L.key);
        if (P !== null && (P.elementType === he || // Keep this check inline so it only runs on the false path:
        b_(P, L) || // Lazy types should reconcile their resolved type.
        // We need to do this after the Hot Reloading check above,
        // because hot reloading has different semantics than prod because
        // it doesn't resuspend. So we can't let the call below suspend.
        typeof he == "object" && he !== null && he.$$typeof === We && SC(he) === P.type)) {
          var de = u(P, L.props);
          return de.ref = bp(N, P, L), de.return = N, de._debugSource = L._source, de._debugOwner = L._owner, de;
        }
        var Ie = sE(L, N.mode, K);
        return Ie.ref = bp(N, P, L), Ie.return = N, Ie;
      }
      function y(N, P, L, K) {
        if (P === null || P.tag !== me || P.stateNode.containerInfo !== L.containerInfo || P.stateNode.implementation !== L.implementation) {
          var he = fE(L, N.mode, K);
          return he.return = N, he;
        } else {
          var de = u(P, L.children || []);
          return de.return = N, de;
        }
      }
      function g(N, P, L, K, he) {
        if (P === null || P.tag !== Et) {
          var de = Xo(L, N.mode, K, he);
          return de.return = N, de;
        } else {
          var Ie = u(P, L);
          return Ie.return = N, Ie;
        }
      }
      function x(N, P, L) {
        if (typeof P == "string" && P !== "" || typeof P == "number") {
          var K = cE("" + P, N.mode, L);
          return K.return = N, K;
        }
        if (typeof P == "object" && P !== null) {
          switch (P.$$typeof) {
            case Dr: {
              var he = sE(P, N.mode, L);
              return he.ref = bp(N, null, P), he.return = N, he;
            }
            case ir: {
              var de = fE(P, N.mode, L);
              return de.return = N, de;
            }
            case We: {
              var Ie = P._payload, Xe = P._init;
              return x(N, Xe(Ie), L);
            }
          }
          if (lt(P) || Je(P)) {
            var Xt = Xo(P, N.mode, L, null);
            return Xt.return = N, Xt;
          }
          Xh(N, P);
        }
        return typeof P == "function" && Zh(N), null;
      }
      function b(N, P, L, K) {
        var he = P !== null ? P.key : null;
        if (typeof L == "string" && L !== "" || typeof L == "number")
          return he !== null ? null : p(N, P, "" + L, K);
        if (typeof L == "object" && L !== null) {
          switch (L.$$typeof) {
            case Dr:
              return L.key === he ? v(N, P, L, K) : null;
            case ir:
              return L.key === he ? y(N, P, L, K) : null;
            case We: {
              var de = L._payload, Ie = L._init;
              return b(N, P, Ie(de), K);
            }
          }
          if (lt(L) || Je(L))
            return he !== null ? null : g(N, P, L, K, null);
          Xh(N, L);
        }
        return typeof L == "function" && Zh(N), null;
      }
      function U(N, P, L, K, he) {
        if (typeof K == "string" && K !== "" || typeof K == "number") {
          var de = N.get(L) || null;
          return p(P, de, "" + K, he);
        }
        if (typeof K == "object" && K !== null) {
          switch (K.$$typeof) {
            case Dr: {
              var Ie = N.get(K.key === null ? L : K.key) || null;
              return v(P, Ie, K, he);
            }
            case ir: {
              var Xe = N.get(K.key === null ? L : K.key) || null;
              return y(P, Xe, K, he);
            }
            case We:
              var Xt = K._payload, At = K._init;
              return U(N, P, L, At(Xt), he);
          }
          if (lt(K) || Je(K)) {
            var Kn = N.get(L) || null;
            return g(P, Kn, K, he, null);
          }
          Xh(P, K);
        }
        return typeof K == "function" && Zh(P), null;
      }
      function F(N, P, L) {
        {
          if (typeof N != "object" || N === null)
            return P;
          switch (N.$$typeof) {
            case Dr:
            case ir:
              gC(N, L);
              var K = N.key;
              if (typeof K != "string")
                break;
              if (P === null) {
                P = /* @__PURE__ */ new Set(), P.add(K);
                break;
              }
              if (!P.has(K)) {
                P.add(K);
                break;
              }
              S("Encountered two children with the same key, `%s`. Keys should be unique so that components maintain their identity across updates. Non-unique keys may cause children to be duplicated and/or omitted — the behavior is unsupported and could change in a future version.", K);
              break;
            case We:
              var he = N._payload, de = N._init;
              F(de(he), P, L);
              break;
          }
        }
        return P;
      }
      function V(N, P, L, K) {
        for (var he = null, de = 0; de < L.length; de++) {
          var Ie = L[de];
          he = F(Ie, he, N);
        }
        for (var Xe = null, Xt = null, At = P, Kn = 0, jt = 0, Pn = null; At !== null && jt < L.length; jt++) {
          At.index > jt ? (Pn = At, At = null) : Pn = At.sibling;
          var sa = b(N, At, L[jt], K);
          if (sa === null) {
            At === null && (At = Pn);
            break;
          }
          e && At && sa.alternate === null && t(N, At), Kn = s(sa, Kn, jt), Xt === null ? Xe = sa : Xt.sibling = sa, Xt = sa, At = Pn;
        }
        if (jt === L.length) {
          if (a(N, At), Fr()) {
            var Yr = jt;
            Js(N, Yr);
          }
          return Xe;
        }
        if (At === null) {
          for (; jt < L.length; jt++) {
            var pi = x(N, L[jt], K);
            pi !== null && (Kn = s(pi, Kn, jt), Xt === null ? Xe = pi : Xt.sibling = pi, Xt = pi);
          }
          if (Fr()) {
            var Ta = jt;
            Js(N, Ta);
          }
          return Xe;
        }
        for (var ba = i(N, At); jt < L.length; jt++) {
          var ca = U(ba, N, jt, L[jt], K);
          ca !== null && (e && ca.alternate !== null && ba.delete(ca.key === null ? jt : ca.key), Kn = s(ca, Kn, jt), Xt === null ? Xe = ca : Xt.sibling = ca, Xt = ca);
        }
        if (e && ba.forEach(function(Zf) {
          return t(N, Zf);
        }), Fr()) {
          var Ju = jt;
          Js(N, Ju);
        }
        return Xe;
      }
      function ce(N, P, L, K) {
        var he = Je(L);
        if (typeof he != "function")
          throw new Error("An object is not an iterable. This error is likely caused by a bug in React. Please file an issue.");
        {
          typeof Symbol == "function" && // $FlowFixMe Flow doesn't know about toStringTag
          L[Symbol.toStringTag] === "Generator" && (dg || S("Using Generators as children is unsupported and will likely yield unexpected results because enumerating a generator mutates it. You may convert it to an array with `Array.from()` or the `[...spread]` operator before rendering. Keep in mind you might need to polyfill these features for older browsers."), dg = !0), L.entries === he && (fg || S("Using Maps as children is not supported. Use an array of keyed ReactElements instead."), fg = !0);
          var de = he.call(L);
          if (de)
            for (var Ie = null, Xe = de.next(); !Xe.done; Xe = de.next()) {
              var Xt = Xe.value;
              Ie = F(Xt, Ie, N);
            }
        }
        var At = he.call(L);
        if (At == null)
          throw new Error("An iterable object provided no iterator.");
        for (var Kn = null, jt = null, Pn = P, sa = 0, Yr = 0, pi = null, Ta = At.next(); Pn !== null && !Ta.done; Yr++, Ta = At.next()) {
          Pn.index > Yr ? (pi = Pn, Pn = null) : pi = Pn.sibling;
          var ba = b(N, Pn, Ta.value, K);
          if (ba === null) {
            Pn === null && (Pn = pi);
            break;
          }
          e && Pn && ba.alternate === null && t(N, Pn), sa = s(ba, sa, Yr), jt === null ? Kn = ba : jt.sibling = ba, jt = ba, Pn = pi;
        }
        if (Ta.done) {
          if (a(N, Pn), Fr()) {
            var ca = Yr;
            Js(N, ca);
          }
          return Kn;
        }
        if (Pn === null) {
          for (; !Ta.done; Yr++, Ta = At.next()) {
            var Ju = x(N, Ta.value, K);
            Ju !== null && (sa = s(Ju, sa, Yr), jt === null ? Kn = Ju : jt.sibling = Ju, jt = Ju);
          }
          if (Fr()) {
            var Zf = Yr;
            Js(N, Zf);
          }
          return Kn;
        }
        for (var rv = i(N, Pn); !Ta.done; Yr++, Ta = At.next()) {
          var iu = U(rv, N, Yr, Ta.value, K);
          iu !== null && (e && iu.alternate !== null && rv.delete(iu.key === null ? Yr : iu.key), sa = s(iu, sa, Yr), jt === null ? Kn = iu : jt.sibling = iu, jt = iu);
        }
        if (e && rv.forEach(function(lk) {
          return t(N, lk);
        }), Fr()) {
          var ik = Yr;
          Js(N, ik);
        }
        return Kn;
      }
      function Ue(N, P, L, K) {
        if (P !== null && P.tag === qe) {
          a(N, P.sibling);
          var he = u(P, L);
          return he.return = N, he;
        }
        a(N, P);
        var de = cE(L, N.mode, K);
        return de.return = N, de;
      }
      function we(N, P, L, K) {
        for (var he = L.key, de = P; de !== null; ) {
          if (de.key === he) {
            var Ie = L.type;
            if (Ie === mi) {
              if (de.tag === Et) {
                a(N, de.sibling);
                var Xe = u(de, L.props.children);
                return Xe.return = N, Xe._debugSource = L._source, Xe._debugOwner = L._owner, Xe;
              }
            } else if (de.elementType === Ie || // Keep this check inline so it only runs on the false path:
            b_(de, L) || // Lazy types should reconcile their resolved type.
            // We need to do this after the Hot Reloading check above,
            // because hot reloading has different semantics than prod because
            // it doesn't resuspend. So we can't let the call below suspend.
            typeof Ie == "object" && Ie !== null && Ie.$$typeof === We && SC(Ie) === de.type) {
              a(N, de.sibling);
              var Xt = u(de, L.props);
              return Xt.ref = bp(N, de, L), Xt.return = N, Xt._debugSource = L._source, Xt._debugOwner = L._owner, Xt;
            }
            a(N, de);
            break;
          } else
            t(N, de);
          de = de.sibling;
        }
        if (L.type === mi) {
          var At = Xo(L.props.children, N.mode, K, L.key);
          return At.return = N, At;
        } else {
          var Kn = sE(L, N.mode, K);
          return Kn.ref = bp(N, P, L), Kn.return = N, Kn;
        }
      }
      function Tt(N, P, L, K) {
        for (var he = L.key, de = P; de !== null; ) {
          if (de.key === he)
            if (de.tag === me && de.stateNode.containerInfo === L.containerInfo && de.stateNode.implementation === L.implementation) {
              a(N, de.sibling);
              var Ie = u(de, L.children || []);
              return Ie.return = N, Ie;
            } else {
              a(N, de);
              break;
            }
          else
            t(N, de);
          de = de.sibling;
        }
        var Xe = fE(L, N.mode, K);
        return Xe.return = N, Xe;
      }
      function gt(N, P, L, K) {
        var he = typeof L == "object" && L !== null && L.type === mi && L.key === null;
        if (he && (L = L.props.children), typeof L == "object" && L !== null) {
          switch (L.$$typeof) {
            case Dr:
              return f(we(N, P, L, K));
            case ir:
              return f(Tt(N, P, L, K));
            case We:
              var de = L._payload, Ie = L._init;
              return gt(N, P, Ie(de), K);
          }
          if (lt(L))
            return V(N, P, L, K);
          if (Je(L))
            return ce(N, P, L, K);
          Xh(N, L);
        }
        return typeof L == "string" && L !== "" || typeof L == "number" ? f(Ue(N, P, "" + L, K)) : (typeof L == "function" && Zh(N), a(N, P));
      }
      return gt;
    }
    var Uf = EC(!0), CC = EC(!1);
    function zb(e, t) {
      if (e !== null && t.child !== e.child)
        throw new Error("Resuming work not yet implemented.");
      if (t.child !== null) {
        var a = t.child, i = dc(a, a.pendingProps);
        for (t.child = i, i.return = t; a.sibling !== null; )
          a = a.sibling, i = i.sibling = dc(a, a.pendingProps), i.return = t;
        i.sibling = null;
      }
    }
    function Ab(e, t) {
      for (var a = e.child; a !== null; )
        Rx(a, t), a = a.sibling;
    }
    var mg = jo(null), yg;
    yg = {};
    var Jh = null, zf = null, gg = null, em = !1;
    function tm() {
      Jh = null, zf = null, gg = null, em = !1;
    }
    function _C() {
      em = !0;
    }
    function RC() {
      em = !1;
    }
    function TC(e, t, a) {
      ua(mg, t._currentValue, e), t._currentValue = a, t._currentRenderer !== void 0 && t._currentRenderer !== null && t._currentRenderer !== yg && S("Detected multiple renderers concurrently rendering the same context provider. This is currently unsupported."), t._currentRenderer = yg;
    }
    function Sg(e, t) {
      var a = mg.current;
      la(mg, t), e._currentValue = a;
    }
    function Eg(e, t, a) {
      for (var i = e; i !== null; ) {
        var u = i.alternate;
        if (zu(i.childLanes, t) ? u !== null && !zu(u.childLanes, t) && (u.childLanes = et(u.childLanes, t)) : (i.childLanes = et(i.childLanes, t), u !== null && (u.childLanes = et(u.childLanes, t))), i === a)
          break;
        i = i.return;
      }
      i !== a && S("Expected to find the propagation root when scheduling context work. This error is likely caused by a bug in React. Please file an issue.");
    }
    function jb(e, t, a) {
      Fb(e, t, a);
    }
    function Fb(e, t, a) {
      var i = e.child;
      for (i !== null && (i.return = e); i !== null; ) {
        var u = void 0, s = i.dependencies;
        if (s !== null) {
          u = i.child;
          for (var f = s.firstContext; f !== null; ) {
            if (f.context === t) {
              if (i.tag === ne) {
                var p = Os(a), v = Wu(Zt, p);
                v.tag = rm;
                var y = i.updateQueue;
                if (y !== null) {
                  var g = y.shared, x = g.pending;
                  x === null ? v.next = v : (v.next = x.next, x.next = v), g.pending = v;
                }
              }
              i.lanes = et(i.lanes, a);
              var b = i.alternate;
              b !== null && (b.lanes = et(b.lanes, a)), Eg(i.return, a, e), s.lanes = et(s.lanes, a);
              break;
            }
            f = f.next;
          }
        } else if (i.tag === ht)
          u = i.type === e.type ? null : i.child;
        else if (i.tag === Jt) {
          var U = i.return;
          if (U === null)
            throw new Error("We just came from a parent so we must have had a parent. This is a bug in React.");
          U.lanes = et(U.lanes, a);
          var F = U.alternate;
          F !== null && (F.lanes = et(F.lanes, a)), Eg(U, a, e), u = i.sibling;
        } else
          u = i.child;
        if (u !== null)
          u.return = i;
        else
          for (u = i; u !== null; ) {
            if (u === e) {
              u = null;
              break;
            }
            var V = u.sibling;
            if (V !== null) {
              V.return = u.return, u = V;
              break;
            }
            u = u.return;
          }
        i = u;
      }
    }
    function Af(e, t) {
      Jh = e, zf = null, gg = null;
      var a = e.dependencies;
      if (a !== null) {
        var i = a.firstContext;
        i !== null && (na(a.lanes, t) && Vp(), a.firstContext = null);
      }
    }
    function rr(e) {
      em && S("Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo().");
      var t = e._currentValue;
      if (gg !== e) {
        var a = {
          context: e,
          memoizedValue: t,
          next: null
        };
        if (zf === null) {
          if (Jh === null)
            throw new Error("Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo().");
          zf = a, Jh.dependencies = {
            lanes: Y,
            firstContext: a
          };
        } else
          zf = zf.next = a;
      }
      return t;
    }
    var ac = null;
    function Cg(e) {
      ac === null ? ac = [e] : ac.push(e);
    }
    function Hb() {
      if (ac !== null) {
        for (var e = 0; e < ac.length; e++) {
          var t = ac[e], a = t.interleaved;
          if (a !== null) {
            t.interleaved = null;
            var i = a.next, u = t.pending;
            if (u !== null) {
              var s = u.next;
              u.next = i, a.next = s;
            }
            t.pending = a;
          }
        }
        ac = null;
      }
    }
    function bC(e, t, a, i) {
      var u = t.interleaved;
      return u === null ? (a.next = a, Cg(t)) : (a.next = u.next, u.next = a), t.interleaved = a, nm(e, i);
    }
    function Vb(e, t, a, i) {
      var u = t.interleaved;
      u === null ? (a.next = a, Cg(t)) : (a.next = u.next, u.next = a), t.interleaved = a;
    }
    function Pb(e, t, a, i) {
      var u = t.interleaved;
      return u === null ? (a.next = a, Cg(t)) : (a.next = u.next, u.next = a), t.interleaved = a, nm(e, i);
    }
    function Ba(e, t) {
      return nm(e, t);
    }
    var Bb = nm;
    function nm(e, t) {
      e.lanes = et(e.lanes, t);
      var a = e.alternate;
      a !== null && (a.lanes = et(a.lanes, t)), a === null && (e.flags & (yn | Xr)) !== Oe && C_(e);
      for (var i = e, u = e.return; u !== null; )
        u.childLanes = et(u.childLanes, t), a = u.alternate, a !== null ? a.childLanes = et(a.childLanes, t) : (u.flags & (yn | Xr)) !== Oe && C_(e), i = u, u = u.return;
      if (i.tag === te) {
        var s = i.stateNode;
        return s;
      } else
        return null;
    }
    var wC = 0, xC = 1, rm = 2, _g = 3, am = !1, Rg, im;
    Rg = !1, im = null;
    function Tg(e) {
      var t = {
        baseState: e.memoizedState,
        firstBaseUpdate: null,
        lastBaseUpdate: null,
        shared: {
          pending: null,
          interleaved: null,
          lanes: Y
        },
        effects: null
      };
      e.updateQueue = t;
    }
    function kC(e, t) {
      var a = t.updateQueue, i = e.updateQueue;
      if (a === i) {
        var u = {
          baseState: i.baseState,
          firstBaseUpdate: i.firstBaseUpdate,
          lastBaseUpdate: i.lastBaseUpdate,
          shared: i.shared,
          effects: i.effects
        };
        t.updateQueue = u;
      }
    }
    function Wu(e, t) {
      var a = {
        eventTime: e,
        lane: t,
        tag: wC,
        payload: null,
        callback: null,
        next: null
      };
      return a;
    }
    function Po(e, t, a) {
      var i = e.updateQueue;
      if (i === null)
        return null;
      var u = i.shared;
      if (im === u && !Rg && (S("An update (setState, replaceState, or forceUpdate) was scheduled from inside an update function. Update functions should be pure, with zero side-effects. Consider using componentDidUpdate or a callback."), Rg = !0), V1()) {
        var s = u.pending;
        return s === null ? t.next = t : (t.next = s.next, s.next = t), u.pending = t, Bb(e, a);
      } else
        return Pb(e, u, t, a);
    }
    function lm(e, t, a) {
      var i = t.updateQueue;
      if (i !== null) {
        var u = i.shared;
        if (Fd(a)) {
          var s = u.lanes;
          s = Vd(s, e.pendingLanes);
          var f = et(s, a);
          u.lanes = f, of(e, f);
        }
      }
    }
    function bg(e, t) {
      var a = e.updateQueue, i = e.alternate;
      if (i !== null) {
        var u = i.updateQueue;
        if (a === u) {
          var s = null, f = null, p = a.firstBaseUpdate;
          if (p !== null) {
            var v = p;
            do {
              var y = {
                eventTime: v.eventTime,
                lane: v.lane,
                tag: v.tag,
                payload: v.payload,
                callback: v.callback,
                next: null
              };
              f === null ? s = f = y : (f.next = y, f = y), v = v.next;
            } while (v !== null);
            f === null ? s = f = t : (f.next = t, f = t);
          } else
            s = f = t;
          a = {
            baseState: u.baseState,
            firstBaseUpdate: s,
            lastBaseUpdate: f,
            shared: u.shared,
            effects: u.effects
          }, e.updateQueue = a;
          return;
        }
      }
      var g = a.lastBaseUpdate;
      g === null ? a.firstBaseUpdate = t : g.next = t, a.lastBaseUpdate = t;
    }
    function $b(e, t, a, i, u, s) {
      switch (a.tag) {
        case xC: {
          var f = a.payload;
          if (typeof f == "function") {
            _C();
            var p = f.call(s, i, u);
            {
              if (e.mode & qt) {
                gn(!0);
                try {
                  f.call(s, i, u);
                } finally {
                  gn(!1);
                }
              }
              RC();
            }
            return p;
          }
          return f;
        }
        case _g:
          e.flags = e.flags & ~Jn | xe;
        case wC: {
          var v = a.payload, y;
          if (typeof v == "function") {
            _C(), y = v.call(s, i, u);
            {
              if (e.mode & qt) {
                gn(!0);
                try {
                  v.call(s, i, u);
                } finally {
                  gn(!1);
                }
              }
              RC();
            }
          } else
            y = v;
          return y == null ? i : nt({}, i, y);
        }
        case rm:
          return am = !0, i;
      }
      return i;
    }
    function um(e, t, a, i) {
      var u = e.updateQueue;
      am = !1, im = u.shared;
      var s = u.firstBaseUpdate, f = u.lastBaseUpdate, p = u.shared.pending;
      if (p !== null) {
        u.shared.pending = null;
        var v = p, y = v.next;
        v.next = null, f === null ? s = y : f.next = y, f = v;
        var g = e.alternate;
        if (g !== null) {
          var x = g.updateQueue, b = x.lastBaseUpdate;
          b !== f && (b === null ? x.firstBaseUpdate = y : b.next = y, x.lastBaseUpdate = v);
        }
      }
      if (s !== null) {
        var U = u.baseState, F = Y, V = null, ce = null, Ue = null, we = s;
        do {
          var Tt = we.lane, gt = we.eventTime;
          if (zu(i, Tt)) {
            if (Ue !== null) {
              var P = {
                eventTime: gt,
                // This update is going to be committed so we never want uncommit
                // it. Using NoLane works because 0 is a subset of all bitmasks, so
                // this will never be skipped by the check above.
                lane: Ot,
                tag: we.tag,
                payload: we.payload,
                callback: we.callback,
                next: null
              };
              Ue = Ue.next = P;
            }
            U = $b(e, u, we, U, t, a);
            var L = we.callback;
            if (L !== null && // If the update was already committed, we should not queue its
            // callback again.
            we.lane !== Ot) {
              e.flags |= an;
              var K = u.effects;
              K === null ? u.effects = [we] : K.push(we);
            }
          } else {
            var N = {
              eventTime: gt,
              lane: Tt,
              tag: we.tag,
              payload: we.payload,
              callback: we.callback,
              next: null
            };
            Ue === null ? (ce = Ue = N, V = U) : Ue = Ue.next = N, F = et(F, Tt);
          }
          if (we = we.next, we === null) {
            if (p = u.shared.pending, p === null)
              break;
            var he = p, de = he.next;
            he.next = null, we = de, u.lastBaseUpdate = he, u.shared.pending = null;
          }
        } while (!0);
        Ue === null && (V = U), u.baseState = V, u.firstBaseUpdate = ce, u.lastBaseUpdate = Ue;
        var Ie = u.shared.interleaved;
        if (Ie !== null) {
          var Xe = Ie;
          do
            F = et(F, Xe.lane), Xe = Xe.next;
          while (Xe !== Ie);
        } else s === null && (u.shared.lanes = Y);
        Zp(F), e.lanes = F, e.memoizedState = U;
      }
      im = null;
    }
    function Ib(e, t) {
      if (typeof e != "function")
        throw new Error("Invalid argument passed as callback. Expected a function. Instead " + ("received: " + e));
      e.call(t);
    }
    function DC() {
      am = !1;
    }
    function om() {
      return am;
    }
    function OC(e, t, a) {
      var i = t.effects;
      if (t.effects = null, i !== null)
        for (var u = 0; u < i.length; u++) {
          var s = i[u], f = s.callback;
          f !== null && (s.callback = null, Ib(f, a));
        }
    }
    var wp = {}, Bo = jo(wp), xp = jo(wp), sm = jo(wp);
    function cm(e) {
      if (e === wp)
        throw new Error("Expected host context to exist. This error is likely caused by a bug in React. Please file an issue.");
      return e;
    }
    function NC() {
      var e = cm(sm.current);
      return e;
    }
    function wg(e, t) {
      ua(sm, t, e), ua(xp, e, e), ua(Bo, wp, e);
      var a = uT(t);
      la(Bo, e), ua(Bo, a, e);
    }
    function jf(e) {
      la(Bo, e), la(xp, e), la(sm, e);
    }
    function xg() {
      var e = cm(Bo.current);
      return e;
    }
    function LC(e) {
      cm(sm.current);
      var t = cm(Bo.current), a = oT(t, e.type);
      t !== a && (ua(xp, e, e), ua(Bo, a, e));
    }
    function kg(e) {
      xp.current === e && (la(Bo, e), la(xp, e));
    }
    var Yb = 0, MC = 1, UC = 1, kp = 2, sl = jo(Yb);
    function Dg(e, t) {
      return (e & t) !== 0;
    }
    function Ff(e) {
      return e & MC;
    }
    function Og(e, t) {
      return e & MC | t;
    }
    function Qb(e, t) {
      return e | t;
    }
    function $o(e, t) {
      ua(sl, t, e);
    }
    function Hf(e) {
      la(sl, e);
    }
    function Wb(e, t) {
      var a = e.memoizedState;
      return a !== null ? a.dehydrated !== null : (e.memoizedProps, !0);
    }
    function fm(e) {
      for (var t = e; t !== null; ) {
        if (t.tag === De) {
          var a = t.memoizedState;
          if (a !== null) {
            var i = a.dehydrated;
            if (i === null || XE(i) || Gy(i))
              return t;
          }
        } else if (t.tag === un && // revealOrder undefined can't be trusted because it don't
        // keep track of whether it suspended or not.
        t.memoizedProps.revealOrder !== void 0) {
          var u = (t.flags & xe) !== Oe;
          if (u)
            return t;
        } else if (t.child !== null) {
          t.child.return = t, t = t.child;
          continue;
        }
        if (t === e)
          return null;
        for (; t.sibling === null; ) {
          if (t.return === null || t.return === e)
            return null;
          t = t.return;
        }
        t.sibling.return = t.return, t = t.sibling;
      }
      return null;
    }
    var $a = (
      /*   */
      0
    ), dr = (
      /* */
      1
    ), Zl = (
      /*  */
      2
    ), pr = (
      /*    */
      4
    ), Hr = (
      /*   */
      8
    ), Ng = [];
    function Lg() {
      for (var e = 0; e < Ng.length; e++) {
        var t = Ng[e];
        t._workInProgressVersionPrimary = null;
      }
      Ng.length = 0;
    }
    function Gb(e, t) {
      var a = t._getVersion, i = a(t._source);
      e.mutableSourceEagerHydrationData == null ? e.mutableSourceEagerHydrationData = [t, i] : e.mutableSourceEagerHydrationData.push(t, i);
    }
    var ve = T.ReactCurrentDispatcher, Dp = T.ReactCurrentBatchConfig, Mg, Vf;
    Mg = /* @__PURE__ */ new Set();
    var ic = Y, Kt = null, vr = null, hr = null, dm = !1, Op = !1, Np = 0, qb = 0, Kb = 25, $ = null, Hi = null, Io = -1, Ug = !1;
    function Bt() {
      {
        var e = $;
        Hi === null ? Hi = [e] : Hi.push(e);
      }
    }
    function ae() {
      {
        var e = $;
        Hi !== null && (Io++, Hi[Io] !== e && Xb(e));
      }
    }
    function Pf(e) {
      e != null && !lt(e) && S("%s received a final argument that is not an array (instead, received `%s`). When specified, the final argument must be an array.", $, typeof e);
    }
    function Xb(e) {
      {
        var t = Qe(Kt);
        if (!Mg.has(t) && (Mg.add(t), Hi !== null)) {
          for (var a = "", i = 30, u = 0; u <= Io; u++) {
            for (var s = Hi[u], f = u === Io ? e : s, p = u + 1 + ". " + s; p.length < i; )
              p += " ";
            p += f + `
`, a += p;
          }
          S(`React has detected a change in the order of Hooks called by %s. This will lead to bugs and errors if not fixed. For more information, read the Rules of Hooks: https://reactjs.org/link/rules-of-hooks

   Previous render            Next render
   ------------------------------------------------------
%s   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`, t, a);
        }
      }
    }
    function oa() {
      throw new Error(`Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://reactjs.org/link/invalid-hook-call for tips about how to debug and fix this problem.`);
    }
    function zg(e, t) {
      if (Ug)
        return !1;
      if (t === null)
        return S("%s received a final argument during this render, but not during the previous render. Even though the final argument is optional, its type cannot change between renders.", $), !1;
      e.length !== t.length && S(`The final argument passed to %s changed size between renders. The order and size of this array must remain constant.

Previous: %s
Incoming: %s`, $, "[" + t.join(", ") + "]", "[" + e.join(", ") + "]");
      for (var a = 0; a < t.length && a < e.length; a++)
        if (!G(e[a], t[a]))
          return !1;
      return !0;
    }
    function Bf(e, t, a, i, u, s) {
      ic = s, Kt = t, Hi = e !== null ? e._debugHookTypes : null, Io = -1, Ug = e !== null && e.type !== t.type, t.memoizedState = null, t.updateQueue = null, t.lanes = Y, e !== null && e.memoizedState !== null ? ve.current = n0 : Hi !== null ? ve.current = t0 : ve.current = e0;
      var f = a(i, u);
      if (Op) {
        var p = 0;
        do {
          if (Op = !1, Np = 0, p >= Kb)
            throw new Error("Too many re-renders. React limits the number of renders to prevent an infinite loop.");
          p += 1, Ug = !1, vr = null, hr = null, t.updateQueue = null, Io = -1, ve.current = r0, f = a(i, u);
        } while (Op);
      }
      ve.current = bm, t._debugHookTypes = Hi;
      var v = vr !== null && vr.next !== null;
      if (ic = Y, Kt = null, vr = null, hr = null, $ = null, Hi = null, Io = -1, e !== null && (e.flags & zn) !== (t.flags & zn) && // Disable this warning in legacy mode, because legacy Suspense is weird
      // and creates false positives. To make this work in legacy mode, we'd
      // need to mark fibers that commit in an incomplete state, somehow. For
      // now I'll disable the warning that most of the bugs that would trigger
      // it are either exclusive to concurrent mode or exist in both.
      (e.mode & ct) !== Ne && S("Internal React error: Expected static flag was missing. Please notify the React team."), dm = !1, v)
        throw new Error("Rendered fewer hooks than expected. This may be caused by an accidental early return statement.");
      return f;
    }
    function $f() {
      var e = Np !== 0;
      return Np = 0, e;
    }
    function zC(e, t, a) {
      t.updateQueue = e.updateQueue, (t.mode & Ut) !== Ne ? t.flags &= -50333701 : t.flags &= -2053, e.lanes = Ns(e.lanes, a);
    }
    function AC() {
      if (ve.current = bm, dm) {
        for (var e = Kt.memoizedState; e !== null; ) {
          var t = e.queue;
          t !== null && (t.pending = null), e = e.next;
        }
        dm = !1;
      }
      ic = Y, Kt = null, vr = null, hr = null, Hi = null, Io = -1, $ = null, qC = !1, Op = !1, Np = 0;
    }
    function Jl() {
      var e = {
        memoizedState: null,
        baseState: null,
        baseQueue: null,
        queue: null,
        next: null
      };
      return hr === null ? Kt.memoizedState = hr = e : hr = hr.next = e, hr;
    }
    function Vi() {
      var e;
      if (vr === null) {
        var t = Kt.alternate;
        t !== null ? e = t.memoizedState : e = null;
      } else
        e = vr.next;
      var a;
      if (hr === null ? a = Kt.memoizedState : a = hr.next, a !== null)
        hr = a, a = hr.next, vr = e;
      else {
        if (e === null)
          throw new Error("Rendered more hooks than during the previous render.");
        vr = e;
        var i = {
          memoizedState: vr.memoizedState,
          baseState: vr.baseState,
          baseQueue: vr.baseQueue,
          queue: vr.queue,
          next: null
        };
        hr === null ? Kt.memoizedState = hr = i : hr = hr.next = i;
      }
      return hr;
    }
    function jC() {
      return {
        lastEffect: null,
        stores: null
      };
    }
    function Ag(e, t) {
      return typeof t == "function" ? t(e) : t;
    }
    function jg(e, t, a) {
      var i = Jl(), u;
      a !== void 0 ? u = a(t) : u = t, i.memoizedState = i.baseState = u;
      var s = {
        pending: null,
        interleaved: null,
        lanes: Y,
        dispatch: null,
        lastRenderedReducer: e,
        lastRenderedState: u
      };
      i.queue = s;
      var f = s.dispatch = tw.bind(null, Kt, s);
      return [i.memoizedState, f];
    }
    function Fg(e, t, a) {
      var i = Vi(), u = i.queue;
      if (u === null)
        throw new Error("Should have a queue. This is likely a bug in React. Please file an issue.");
      u.lastRenderedReducer = e;
      var s = vr, f = s.baseQueue, p = u.pending;
      if (p !== null) {
        if (f !== null) {
          var v = f.next, y = p.next;
          f.next = y, p.next = v;
        }
        s.baseQueue !== f && S("Internal error: Expected work-in-progress queue to be a clone. This is a bug in React."), s.baseQueue = f = p, u.pending = null;
      }
      if (f !== null) {
        var g = f.next, x = s.baseState, b = null, U = null, F = null, V = g;
        do {
          var ce = V.lane;
          if (zu(ic, ce)) {
            if (F !== null) {
              var we = {
                // This update is going to be committed so we never want uncommit
                // it. Using NoLane works because 0 is a subset of all bitmasks, so
                // this will never be skipped by the check above.
                lane: Ot,
                action: V.action,
                hasEagerState: V.hasEagerState,
                eagerState: V.eagerState,
                next: null
              };
              F = F.next = we;
            }
            if (V.hasEagerState)
              x = V.eagerState;
            else {
              var Tt = V.action;
              x = e(x, Tt);
            }
          } else {
            var Ue = {
              lane: ce,
              action: V.action,
              hasEagerState: V.hasEagerState,
              eagerState: V.eagerState,
              next: null
            };
            F === null ? (U = F = Ue, b = x) : F = F.next = Ue, Kt.lanes = et(Kt.lanes, ce), Zp(ce);
          }
          V = V.next;
        } while (V !== null && V !== g);
        F === null ? b = x : F.next = U, G(x, i.memoizedState) || Vp(), i.memoizedState = x, i.baseState = b, i.baseQueue = F, u.lastRenderedState = x;
      }
      var gt = u.interleaved;
      if (gt !== null) {
        var N = gt;
        do {
          var P = N.lane;
          Kt.lanes = et(Kt.lanes, P), Zp(P), N = N.next;
        } while (N !== gt);
      } else f === null && (u.lanes = Y);
      var L = u.dispatch;
      return [i.memoizedState, L];
    }
    function Hg(e, t, a) {
      var i = Vi(), u = i.queue;
      if (u === null)
        throw new Error("Should have a queue. This is likely a bug in React. Please file an issue.");
      u.lastRenderedReducer = e;
      var s = u.dispatch, f = u.pending, p = i.memoizedState;
      if (f !== null) {
        u.pending = null;
        var v = f.next, y = v;
        do {
          var g = y.action;
          p = e(p, g), y = y.next;
        } while (y !== v);
        G(p, i.memoizedState) || Vp(), i.memoizedState = p, i.baseQueue === null && (i.baseState = p), u.lastRenderedState = p;
      }
      return [p, s];
    }
    function zD(e, t, a) {
    }
    function AD(e, t, a) {
    }
    function Vg(e, t, a) {
      var i = Kt, u = Jl(), s, f = Fr();
      if (f) {
        if (a === void 0)
          throw new Error("Missing getServerSnapshot, which is required for server-rendered content. Will revert to client rendering.");
        s = a(), Vf || s !== a() && (S("The result of getServerSnapshot should be cached to avoid an infinite loop"), Vf = !0);
      } else {
        if (s = t(), !Vf) {
          var p = t();
          G(s, p) || (S("The result of getSnapshot should be cached to avoid an infinite loop"), Vf = !0);
        }
        var v = Im();
        if (v === null)
          throw new Error("Expected a work-in-progress root. This is a bug in React. Please file an issue.");
        lf(v, ic) || FC(i, t, s);
      }
      u.memoizedState = s;
      var y = {
        value: s,
        getSnapshot: t
      };
      return u.queue = y, ym(VC.bind(null, i, y, e), [e]), i.flags |= Kr, Lp(dr | Hr, HC.bind(null, i, y, s, t), void 0, null), s;
    }
    function pm(e, t, a) {
      var i = Kt, u = Vi(), s = t();
      if (!Vf) {
        var f = t();
        G(s, f) || (S("The result of getSnapshot should be cached to avoid an infinite loop"), Vf = !0);
      }
      var p = u.memoizedState, v = !G(p, s);
      v && (u.memoizedState = s, Vp());
      var y = u.queue;
      if (Up(VC.bind(null, i, y, e), [e]), y.getSnapshot !== t || v || // Check if the susbcribe function changed. We can save some memory by
      // checking whether we scheduled a subscription effect above.
      hr !== null && hr.memoizedState.tag & dr) {
        i.flags |= Kr, Lp(dr | Hr, HC.bind(null, i, y, s, t), void 0, null);
        var g = Im();
        if (g === null)
          throw new Error("Expected a work-in-progress root. This is a bug in React. Please file an issue.");
        lf(g, ic) || FC(i, t, s);
      }
      return s;
    }
    function FC(e, t, a) {
      e.flags |= Co;
      var i = {
        getSnapshot: t,
        value: a
      }, u = Kt.updateQueue;
      if (u === null)
        u = jC(), Kt.updateQueue = u, u.stores = [i];
      else {
        var s = u.stores;
        s === null ? u.stores = [i] : s.push(i);
      }
    }
    function HC(e, t, a, i) {
      t.value = a, t.getSnapshot = i, PC(t) && BC(e);
    }
    function VC(e, t, a) {
      var i = function() {
        PC(t) && BC(e);
      };
      return a(i);
    }
    function PC(e) {
      var t = e.getSnapshot, a = e.value;
      try {
        var i = t();
        return !G(a, i);
      } catch {
        return !0;
      }
    }
    function BC(e) {
      var t = Ba(e, Pe);
      t !== null && Sr(t, e, Pe, Zt);
    }
    function vm(e) {
      var t = Jl();
      typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e;
      var a = {
        pending: null,
        interleaved: null,
        lanes: Y,
        dispatch: null,
        lastRenderedReducer: Ag,
        lastRenderedState: e
      };
      t.queue = a;
      var i = a.dispatch = nw.bind(null, Kt, a);
      return [t.memoizedState, i];
    }
    function Pg(e) {
      return Fg(Ag);
    }
    function Bg(e) {
      return Hg(Ag);
    }
    function Lp(e, t, a, i) {
      var u = {
        tag: e,
        create: t,
        destroy: a,
        deps: i,
        // Circular
        next: null
      }, s = Kt.updateQueue;
      if (s === null)
        s = jC(), Kt.updateQueue = s, s.lastEffect = u.next = u;
      else {
        var f = s.lastEffect;
        if (f === null)
          s.lastEffect = u.next = u;
        else {
          var p = f.next;
          f.next = u, u.next = p, s.lastEffect = u;
        }
      }
      return u;
    }
    function $g(e) {
      var t = Jl();
      {
        var a = {
          current: e
        };
        return t.memoizedState = a, a;
      }
    }
    function hm(e) {
      var t = Vi();
      return t.memoizedState;
    }
    function Mp(e, t, a, i) {
      var u = Jl(), s = i === void 0 ? null : i;
      Kt.flags |= e, u.memoizedState = Lp(dr | t, a, void 0, s);
    }
    function mm(e, t, a, i) {
      var u = Vi(), s = i === void 0 ? null : i, f = void 0;
      if (vr !== null) {
        var p = vr.memoizedState;
        if (f = p.destroy, s !== null) {
          var v = p.deps;
          if (zg(s, v)) {
            u.memoizedState = Lp(t, a, f, s);
            return;
          }
        }
      }
      Kt.flags |= e, u.memoizedState = Lp(dr | t, a, f, s);
    }
    function ym(e, t) {
      return (Kt.mode & Ut) !== Ne ? Mp(xi | Kr | Lc, Hr, e, t) : Mp(Kr | Lc, Hr, e, t);
    }
    function Up(e, t) {
      return mm(Kr, Hr, e, t);
    }
    function Ig(e, t) {
      return Mp(Ct, Zl, e, t);
    }
    function gm(e, t) {
      return mm(Ct, Zl, e, t);
    }
    function Yg(e, t) {
      var a = Ct;
      return a |= Xi, (Kt.mode & Ut) !== Ne && (a |= Ul), Mp(a, pr, e, t);
    }
    function Sm(e, t) {
      return mm(Ct, pr, e, t);
    }
    function $C(e, t) {
      if (typeof t == "function") {
        var a = t, i = e();
        return a(i), function() {
          a(null);
        };
      } else if (t != null) {
        var u = t;
        u.hasOwnProperty("current") || S("Expected useImperativeHandle() first argument to either be a ref callback or React.createRef() object. Instead received: %s.", "an object with keys {" + Object.keys(u).join(", ") + "}");
        var s = e();
        return u.current = s, function() {
          u.current = null;
        };
      }
    }
    function Qg(e, t, a) {
      typeof t != "function" && S("Expected useImperativeHandle() second argument to be a function that creates a handle. Instead received: %s.", t !== null ? typeof t : "null");
      var i = a != null ? a.concat([e]) : null, u = Ct;
      return u |= Xi, (Kt.mode & Ut) !== Ne && (u |= Ul), Mp(u, pr, $C.bind(null, t, e), i);
    }
    function Em(e, t, a) {
      typeof t != "function" && S("Expected useImperativeHandle() second argument to be a function that creates a handle. Instead received: %s.", t !== null ? typeof t : "null");
      var i = a != null ? a.concat([e]) : null;
      return mm(Ct, pr, $C.bind(null, t, e), i);
    }
    function Zb(e, t) {
    }
    var Cm = Zb;
    function Wg(e, t) {
      var a = Jl(), i = t === void 0 ? null : t;
      return a.memoizedState = [e, i], e;
    }
    function _m(e, t) {
      var a = Vi(), i = t === void 0 ? null : t, u = a.memoizedState;
      if (u !== null && i !== null) {
        var s = u[1];
        if (zg(i, s))
          return u[0];
      }
      return a.memoizedState = [e, i], e;
    }
    function Gg(e, t) {
      var a = Jl(), i = t === void 0 ? null : t, u = e();
      return a.memoizedState = [u, i], u;
    }
    function Rm(e, t) {
      var a = Vi(), i = t === void 0 ? null : t, u = a.memoizedState;
      if (u !== null && i !== null) {
        var s = u[1];
        if (zg(i, s))
          return u[0];
      }
      var f = e();
      return a.memoizedState = [f, i], f;
    }
    function qg(e) {
      var t = Jl();
      return t.memoizedState = e, e;
    }
    function IC(e) {
      var t = Vi(), a = vr, i = a.memoizedState;
      return QC(t, i, e);
    }
    function YC(e) {
      var t = Vi();
      if (vr === null)
        return t.memoizedState = e, e;
      var a = vr.memoizedState;
      return QC(t, a, e);
    }
    function QC(e, t, a) {
      var i = !Ad(ic);
      if (i) {
        if (!G(a, t)) {
          var u = Hd();
          Kt.lanes = et(Kt.lanes, u), Zp(u), e.baseState = !0;
        }
        return t;
      } else
        return e.baseState && (e.baseState = !1, Vp()), e.memoizedState = a, a;
    }
    function Jb(e, t, a) {
      var i = Ha();
      Fn(eh(i, Ni)), e(!0);
      var u = Dp.transition;
      Dp.transition = {};
      var s = Dp.transition;
      Dp.transition._updatedFibers = /* @__PURE__ */ new Set();
      try {
        e(!1), t();
      } finally {
        if (Fn(i), Dp.transition = u, u === null && s._updatedFibers) {
          var f = s._updatedFibers.size;
          f > 10 && He("Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table."), s._updatedFibers.clear();
        }
      }
    }
    function Kg() {
      var e = vm(!1), t = e[0], a = e[1], i = Jb.bind(null, a), u = Jl();
      return u.memoizedState = i, [t, i];
    }
    function WC() {
      var e = Pg(), t = e[0], a = Vi(), i = a.memoizedState;
      return [t, i];
    }
    function GC() {
      var e = Bg(), t = e[0], a = Vi(), i = a.memoizedState;
      return [t, i];
    }
    var qC = !1;
    function ew() {
      return qC;
    }
    function Xg() {
      var e = Jl(), t = Im(), a = t.identifierPrefix, i;
      if (Fr()) {
        var u = yb();
        i = ":" + a + "R" + u;
        var s = Np++;
        s > 0 && (i += "H" + s.toString(32)), i += ":";
      } else {
        var f = qb++;
        i = ":" + a + "r" + f.toString(32) + ":";
      }
      return e.memoizedState = i, i;
    }
    function Tm() {
      var e = Vi(), t = e.memoizedState;
      return t;
    }
    function tw(e, t, a) {
      typeof arguments[3] == "function" && S("State updates from the useState() and useReducer() Hooks don't support the second callback argument. To execute a side effect after rendering, declare it in the component body with useEffect().");
      var i = qo(e), u = {
        lane: i,
        action: a,
        hasEagerState: !1,
        eagerState: null,
        next: null
      };
      if (KC(e))
        XC(t, u);
      else {
        var s = bC(e, t, u, i);
        if (s !== null) {
          var f = Ra();
          Sr(s, e, i, f), ZC(s, t, i);
        }
      }
      JC(e, i);
    }
    function nw(e, t, a) {
      typeof arguments[3] == "function" && S("State updates from the useState() and useReducer() Hooks don't support the second callback argument. To execute a side effect after rendering, declare it in the component body with useEffect().");
      var i = qo(e), u = {
        lane: i,
        action: a,
        hasEagerState: !1,
        eagerState: null,
        next: null
      };
      if (KC(e))
        XC(t, u);
      else {
        var s = e.alternate;
        if (e.lanes === Y && (s === null || s.lanes === Y)) {
          var f = t.lastRenderedReducer;
          if (f !== null) {
            var p;
            p = ve.current, ve.current = cl;
            try {
              var v = t.lastRenderedState, y = f(v, a);
              if (u.hasEagerState = !0, u.eagerState = y, G(y, v)) {
                Vb(e, t, u, i);
                return;
              }
            } catch {
            } finally {
              ve.current = p;
            }
          }
        }
        var g = bC(e, t, u, i);
        if (g !== null) {
          var x = Ra();
          Sr(g, e, i, x), ZC(g, t, i);
        }
      }
      JC(e, i);
    }
    function KC(e) {
      var t = e.alternate;
      return e === Kt || t !== null && t === Kt;
    }
    function XC(e, t) {
      Op = dm = !0;
      var a = e.pending;
      a === null ? t.next = t : (t.next = a.next, a.next = t), e.pending = t;
    }
    function ZC(e, t, a) {
      if (Fd(a)) {
        var i = t.lanes;
        i = Vd(i, e.pendingLanes);
        var u = et(i, a);
        t.lanes = u, of(e, u);
      }
    }
    function JC(e, t, a) {
      Cs(e, t);
    }
    var bm = {
      readContext: rr,
      useCallback: oa,
      useContext: oa,
      useEffect: oa,
      useImperativeHandle: oa,
      useInsertionEffect: oa,
      useLayoutEffect: oa,
      useMemo: oa,
      useReducer: oa,
      useRef: oa,
      useState: oa,
      useDebugValue: oa,
      useDeferredValue: oa,
      useTransition: oa,
      useMutableSource: oa,
      useSyncExternalStore: oa,
      useId: oa,
      unstable_isNewReconciler: J
    }, e0 = null, t0 = null, n0 = null, r0 = null, eu = null, cl = null, wm = null;
    {
      var Zg = function() {
        S("Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo().");
      }, Ge = function() {
        S("Do not call Hooks inside useEffect(...), useMemo(...), or other built-in Hooks. You can only call Hooks at the top level of your React function. For more information, see https://reactjs.org/link/rules-of-hooks");
      };
      e0 = {
        readContext: function(e) {
          return rr(e);
        },
        useCallback: function(e, t) {
          return $ = "useCallback", Bt(), Pf(t), Wg(e, t);
        },
        useContext: function(e) {
          return $ = "useContext", Bt(), rr(e);
        },
        useEffect: function(e, t) {
          return $ = "useEffect", Bt(), Pf(t), ym(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return $ = "useImperativeHandle", Bt(), Pf(a), Qg(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return $ = "useInsertionEffect", Bt(), Pf(t), Ig(e, t);
        },
        useLayoutEffect: function(e, t) {
          return $ = "useLayoutEffect", Bt(), Pf(t), Yg(e, t);
        },
        useMemo: function(e, t) {
          $ = "useMemo", Bt(), Pf(t);
          var a = ve.current;
          ve.current = eu;
          try {
            return Gg(e, t);
          } finally {
            ve.current = a;
          }
        },
        useReducer: function(e, t, a) {
          $ = "useReducer", Bt();
          var i = ve.current;
          ve.current = eu;
          try {
            return jg(e, t, a);
          } finally {
            ve.current = i;
          }
        },
        useRef: function(e) {
          return $ = "useRef", Bt(), $g(e);
        },
        useState: function(e) {
          $ = "useState", Bt();
          var t = ve.current;
          ve.current = eu;
          try {
            return vm(e);
          } finally {
            ve.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return $ = "useDebugValue", Bt(), void 0;
        },
        useDeferredValue: function(e) {
          return $ = "useDeferredValue", Bt(), qg(e);
        },
        useTransition: function() {
          return $ = "useTransition", Bt(), Kg();
        },
        useMutableSource: function(e, t, a) {
          return $ = "useMutableSource", Bt(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return $ = "useSyncExternalStore", Bt(), Vg(e, t, a);
        },
        useId: function() {
          return $ = "useId", Bt(), Xg();
        },
        unstable_isNewReconciler: J
      }, t0 = {
        readContext: function(e) {
          return rr(e);
        },
        useCallback: function(e, t) {
          return $ = "useCallback", ae(), Wg(e, t);
        },
        useContext: function(e) {
          return $ = "useContext", ae(), rr(e);
        },
        useEffect: function(e, t) {
          return $ = "useEffect", ae(), ym(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return $ = "useImperativeHandle", ae(), Qg(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return $ = "useInsertionEffect", ae(), Ig(e, t);
        },
        useLayoutEffect: function(e, t) {
          return $ = "useLayoutEffect", ae(), Yg(e, t);
        },
        useMemo: function(e, t) {
          $ = "useMemo", ae();
          var a = ve.current;
          ve.current = eu;
          try {
            return Gg(e, t);
          } finally {
            ve.current = a;
          }
        },
        useReducer: function(e, t, a) {
          $ = "useReducer", ae();
          var i = ve.current;
          ve.current = eu;
          try {
            return jg(e, t, a);
          } finally {
            ve.current = i;
          }
        },
        useRef: function(e) {
          return $ = "useRef", ae(), $g(e);
        },
        useState: function(e) {
          $ = "useState", ae();
          var t = ve.current;
          ve.current = eu;
          try {
            return vm(e);
          } finally {
            ve.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return $ = "useDebugValue", ae(), void 0;
        },
        useDeferredValue: function(e) {
          return $ = "useDeferredValue", ae(), qg(e);
        },
        useTransition: function() {
          return $ = "useTransition", ae(), Kg();
        },
        useMutableSource: function(e, t, a) {
          return $ = "useMutableSource", ae(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return $ = "useSyncExternalStore", ae(), Vg(e, t, a);
        },
        useId: function() {
          return $ = "useId", ae(), Xg();
        },
        unstable_isNewReconciler: J
      }, n0 = {
        readContext: function(e) {
          return rr(e);
        },
        useCallback: function(e, t) {
          return $ = "useCallback", ae(), _m(e, t);
        },
        useContext: function(e) {
          return $ = "useContext", ae(), rr(e);
        },
        useEffect: function(e, t) {
          return $ = "useEffect", ae(), Up(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return $ = "useImperativeHandle", ae(), Em(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return $ = "useInsertionEffect", ae(), gm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return $ = "useLayoutEffect", ae(), Sm(e, t);
        },
        useMemo: function(e, t) {
          $ = "useMemo", ae();
          var a = ve.current;
          ve.current = cl;
          try {
            return Rm(e, t);
          } finally {
            ve.current = a;
          }
        },
        useReducer: function(e, t, a) {
          $ = "useReducer", ae();
          var i = ve.current;
          ve.current = cl;
          try {
            return Fg(e, t, a);
          } finally {
            ve.current = i;
          }
        },
        useRef: function(e) {
          return $ = "useRef", ae(), hm();
        },
        useState: function(e) {
          $ = "useState", ae();
          var t = ve.current;
          ve.current = cl;
          try {
            return Pg(e);
          } finally {
            ve.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return $ = "useDebugValue", ae(), Cm();
        },
        useDeferredValue: function(e) {
          return $ = "useDeferredValue", ae(), IC(e);
        },
        useTransition: function() {
          return $ = "useTransition", ae(), WC();
        },
        useMutableSource: function(e, t, a) {
          return $ = "useMutableSource", ae(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return $ = "useSyncExternalStore", ae(), pm(e, t);
        },
        useId: function() {
          return $ = "useId", ae(), Tm();
        },
        unstable_isNewReconciler: J
      }, r0 = {
        readContext: function(e) {
          return rr(e);
        },
        useCallback: function(e, t) {
          return $ = "useCallback", ae(), _m(e, t);
        },
        useContext: function(e) {
          return $ = "useContext", ae(), rr(e);
        },
        useEffect: function(e, t) {
          return $ = "useEffect", ae(), Up(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return $ = "useImperativeHandle", ae(), Em(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return $ = "useInsertionEffect", ae(), gm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return $ = "useLayoutEffect", ae(), Sm(e, t);
        },
        useMemo: function(e, t) {
          $ = "useMemo", ae();
          var a = ve.current;
          ve.current = wm;
          try {
            return Rm(e, t);
          } finally {
            ve.current = a;
          }
        },
        useReducer: function(e, t, a) {
          $ = "useReducer", ae();
          var i = ve.current;
          ve.current = wm;
          try {
            return Hg(e, t, a);
          } finally {
            ve.current = i;
          }
        },
        useRef: function(e) {
          return $ = "useRef", ae(), hm();
        },
        useState: function(e) {
          $ = "useState", ae();
          var t = ve.current;
          ve.current = wm;
          try {
            return Bg(e);
          } finally {
            ve.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return $ = "useDebugValue", ae(), Cm();
        },
        useDeferredValue: function(e) {
          return $ = "useDeferredValue", ae(), YC(e);
        },
        useTransition: function() {
          return $ = "useTransition", ae(), GC();
        },
        useMutableSource: function(e, t, a) {
          return $ = "useMutableSource", ae(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return $ = "useSyncExternalStore", ae(), pm(e, t);
        },
        useId: function() {
          return $ = "useId", ae(), Tm();
        },
        unstable_isNewReconciler: J
      }, eu = {
        readContext: function(e) {
          return Zg(), rr(e);
        },
        useCallback: function(e, t) {
          return $ = "useCallback", Ge(), Bt(), Wg(e, t);
        },
        useContext: function(e) {
          return $ = "useContext", Ge(), Bt(), rr(e);
        },
        useEffect: function(e, t) {
          return $ = "useEffect", Ge(), Bt(), ym(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return $ = "useImperativeHandle", Ge(), Bt(), Qg(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return $ = "useInsertionEffect", Ge(), Bt(), Ig(e, t);
        },
        useLayoutEffect: function(e, t) {
          return $ = "useLayoutEffect", Ge(), Bt(), Yg(e, t);
        },
        useMemo: function(e, t) {
          $ = "useMemo", Ge(), Bt();
          var a = ve.current;
          ve.current = eu;
          try {
            return Gg(e, t);
          } finally {
            ve.current = a;
          }
        },
        useReducer: function(e, t, a) {
          $ = "useReducer", Ge(), Bt();
          var i = ve.current;
          ve.current = eu;
          try {
            return jg(e, t, a);
          } finally {
            ve.current = i;
          }
        },
        useRef: function(e) {
          return $ = "useRef", Ge(), Bt(), $g(e);
        },
        useState: function(e) {
          $ = "useState", Ge(), Bt();
          var t = ve.current;
          ve.current = eu;
          try {
            return vm(e);
          } finally {
            ve.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return $ = "useDebugValue", Ge(), Bt(), void 0;
        },
        useDeferredValue: function(e) {
          return $ = "useDeferredValue", Ge(), Bt(), qg(e);
        },
        useTransition: function() {
          return $ = "useTransition", Ge(), Bt(), Kg();
        },
        useMutableSource: function(e, t, a) {
          return $ = "useMutableSource", Ge(), Bt(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return $ = "useSyncExternalStore", Ge(), Bt(), Vg(e, t, a);
        },
        useId: function() {
          return $ = "useId", Ge(), Bt(), Xg();
        },
        unstable_isNewReconciler: J
      }, cl = {
        readContext: function(e) {
          return Zg(), rr(e);
        },
        useCallback: function(e, t) {
          return $ = "useCallback", Ge(), ae(), _m(e, t);
        },
        useContext: function(e) {
          return $ = "useContext", Ge(), ae(), rr(e);
        },
        useEffect: function(e, t) {
          return $ = "useEffect", Ge(), ae(), Up(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return $ = "useImperativeHandle", Ge(), ae(), Em(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return $ = "useInsertionEffect", Ge(), ae(), gm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return $ = "useLayoutEffect", Ge(), ae(), Sm(e, t);
        },
        useMemo: function(e, t) {
          $ = "useMemo", Ge(), ae();
          var a = ve.current;
          ve.current = cl;
          try {
            return Rm(e, t);
          } finally {
            ve.current = a;
          }
        },
        useReducer: function(e, t, a) {
          $ = "useReducer", Ge(), ae();
          var i = ve.current;
          ve.current = cl;
          try {
            return Fg(e, t, a);
          } finally {
            ve.current = i;
          }
        },
        useRef: function(e) {
          return $ = "useRef", Ge(), ae(), hm();
        },
        useState: function(e) {
          $ = "useState", Ge(), ae();
          var t = ve.current;
          ve.current = cl;
          try {
            return Pg(e);
          } finally {
            ve.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return $ = "useDebugValue", Ge(), ae(), Cm();
        },
        useDeferredValue: function(e) {
          return $ = "useDeferredValue", Ge(), ae(), IC(e);
        },
        useTransition: function() {
          return $ = "useTransition", Ge(), ae(), WC();
        },
        useMutableSource: function(e, t, a) {
          return $ = "useMutableSource", Ge(), ae(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return $ = "useSyncExternalStore", Ge(), ae(), pm(e, t);
        },
        useId: function() {
          return $ = "useId", Ge(), ae(), Tm();
        },
        unstable_isNewReconciler: J
      }, wm = {
        readContext: function(e) {
          return Zg(), rr(e);
        },
        useCallback: function(e, t) {
          return $ = "useCallback", Ge(), ae(), _m(e, t);
        },
        useContext: function(e) {
          return $ = "useContext", Ge(), ae(), rr(e);
        },
        useEffect: function(e, t) {
          return $ = "useEffect", Ge(), ae(), Up(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return $ = "useImperativeHandle", Ge(), ae(), Em(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return $ = "useInsertionEffect", Ge(), ae(), gm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return $ = "useLayoutEffect", Ge(), ae(), Sm(e, t);
        },
        useMemo: function(e, t) {
          $ = "useMemo", Ge(), ae();
          var a = ve.current;
          ve.current = cl;
          try {
            return Rm(e, t);
          } finally {
            ve.current = a;
          }
        },
        useReducer: function(e, t, a) {
          $ = "useReducer", Ge(), ae();
          var i = ve.current;
          ve.current = cl;
          try {
            return Hg(e, t, a);
          } finally {
            ve.current = i;
          }
        },
        useRef: function(e) {
          return $ = "useRef", Ge(), ae(), hm();
        },
        useState: function(e) {
          $ = "useState", Ge(), ae();
          var t = ve.current;
          ve.current = cl;
          try {
            return Bg(e);
          } finally {
            ve.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return $ = "useDebugValue", Ge(), ae(), Cm();
        },
        useDeferredValue: function(e) {
          return $ = "useDeferredValue", Ge(), ae(), YC(e);
        },
        useTransition: function() {
          return $ = "useTransition", Ge(), ae(), GC();
        },
        useMutableSource: function(e, t, a) {
          return $ = "useMutableSource", Ge(), ae(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return $ = "useSyncExternalStore", Ge(), ae(), pm(e, t);
        },
        useId: function() {
          return $ = "useId", Ge(), ae(), Tm();
        },
        unstable_isNewReconciler: J
      };
    }
    var Yo = A.unstable_now, a0 = 0, xm = -1, zp = -1, km = -1, Jg = !1, Dm = !1;
    function i0() {
      return Jg;
    }
    function rw() {
      Dm = !0;
    }
    function aw() {
      Jg = !1, Dm = !1;
    }
    function iw() {
      Jg = Dm, Dm = !1;
    }
    function l0() {
      return a0;
    }
    function u0() {
      a0 = Yo();
    }
    function eS(e) {
      zp = Yo(), e.actualStartTime < 0 && (e.actualStartTime = Yo());
    }
    function o0(e) {
      zp = -1;
    }
    function Om(e, t) {
      if (zp >= 0) {
        var a = Yo() - zp;
        e.actualDuration += a, t && (e.selfBaseDuration = a), zp = -1;
      }
    }
    function tu(e) {
      if (xm >= 0) {
        var t = Yo() - xm;
        xm = -1;
        for (var a = e.return; a !== null; ) {
          switch (a.tag) {
            case te:
              var i = a.stateNode;
              i.effectDuration += t;
              return;
            case yt:
              var u = a.stateNode;
              u.effectDuration += t;
              return;
          }
          a = a.return;
        }
      }
    }
    function tS(e) {
      if (km >= 0) {
        var t = Yo() - km;
        km = -1;
        for (var a = e.return; a !== null; ) {
          switch (a.tag) {
            case te:
              var i = a.stateNode;
              i !== null && (i.passiveEffectDuration += t);
              return;
            case yt:
              var u = a.stateNode;
              u !== null && (u.passiveEffectDuration += t);
              return;
          }
          a = a.return;
        }
      }
    }
    function nu() {
      xm = Yo();
    }
    function nS() {
      km = Yo();
    }
    function rS(e) {
      for (var t = e.child; t; )
        e.actualDuration += t.actualDuration, t = t.sibling;
    }
    function fl(e, t) {
      if (e && e.defaultProps) {
        var a = nt({}, t), i = e.defaultProps;
        for (var u in i)
          a[u] === void 0 && (a[u] = i[u]);
        return a;
      }
      return t;
    }
    var aS = {}, iS, lS, uS, oS, sS, s0, Nm, cS, fS, dS, Ap;
    {
      iS = /* @__PURE__ */ new Set(), lS = /* @__PURE__ */ new Set(), uS = /* @__PURE__ */ new Set(), oS = /* @__PURE__ */ new Set(), cS = /* @__PURE__ */ new Set(), sS = /* @__PURE__ */ new Set(), fS = /* @__PURE__ */ new Set(), dS = /* @__PURE__ */ new Set(), Ap = /* @__PURE__ */ new Set();
      var c0 = /* @__PURE__ */ new Set();
      Nm = function(e, t) {
        if (!(e === null || typeof e == "function")) {
          var a = t + "_" + e;
          c0.has(a) || (c0.add(a), S("%s(...): Expected the last optional `callback` argument to be a function. Instead received: %s.", t, e));
        }
      }, s0 = function(e, t) {
        if (t === void 0) {
          var a = wt(e) || "Component";
          sS.has(a) || (sS.add(a), S("%s.getDerivedStateFromProps(): A valid state object (or null) must be returned. You have returned undefined.", a));
        }
      }, Object.defineProperty(aS, "_processChildContext", {
        enumerable: !1,
        value: function() {
          throw new Error("_processChildContext is not available in React 16+. This likely means you have multiple copies of React and are attempting to nest a React 15 tree inside a React 16 tree using unstable_renderSubtreeIntoContainer, which isn't supported. Try to make sure you have only one copy of React (and ideally, switch to ReactDOM.createPortal).");
        }
      }), Object.freeze(aS);
    }
    function pS(e, t, a, i) {
      var u = e.memoizedState, s = a(i, u);
      {
        if (e.mode & qt) {
          gn(!0);
          try {
            s = a(i, u);
          } finally {
            gn(!1);
          }
        }
        s0(t, s);
      }
      var f = s == null ? u : nt({}, u, s);
      if (e.memoizedState = f, e.lanes === Y) {
        var p = e.updateQueue;
        p.baseState = f;
      }
    }
    var vS = {
      isMounted: Fv,
      enqueueSetState: function(e, t, a) {
        var i = Eo(e), u = Ra(), s = qo(i), f = Wu(u, s);
        f.payload = t, a != null && (Nm(a, "setState"), f.callback = a);
        var p = Po(i, f, s);
        p !== null && (Sr(p, i, s, u), lm(p, i, s)), Cs(i, s);
      },
      enqueueReplaceState: function(e, t, a) {
        var i = Eo(e), u = Ra(), s = qo(i), f = Wu(u, s);
        f.tag = xC, f.payload = t, a != null && (Nm(a, "replaceState"), f.callback = a);
        var p = Po(i, f, s);
        p !== null && (Sr(p, i, s, u), lm(p, i, s)), Cs(i, s);
      },
      enqueueForceUpdate: function(e, t) {
        var a = Eo(e), i = Ra(), u = qo(a), s = Wu(i, u);
        s.tag = rm, t != null && (Nm(t, "forceUpdate"), s.callback = t);
        var f = Po(a, s, u);
        f !== null && (Sr(f, a, u, i), lm(f, a, u)), Hc(a, u);
      }
    };
    function f0(e, t, a, i, u, s, f) {
      var p = e.stateNode;
      if (typeof p.shouldComponentUpdate == "function") {
        var v = p.shouldComponentUpdate(i, s, f);
        {
          if (e.mode & qt) {
            gn(!0);
            try {
              v = p.shouldComponentUpdate(i, s, f);
            } finally {
              gn(!1);
            }
          }
          v === void 0 && S("%s.shouldComponentUpdate(): Returned undefined instead of a boolean value. Make sure to return true or false.", wt(t) || "Component");
        }
        return v;
      }
      return t.prototype && t.prototype.isPureReactComponent ? !Ee(a, i) || !Ee(u, s) : !0;
    }
    function lw(e, t, a) {
      var i = e.stateNode;
      {
        var u = wt(t) || "Component", s = i.render;
        s || (t.prototype && typeof t.prototype.render == "function" ? S("%s(...): No `render` method found on the returned component instance: did you accidentally return an object from the constructor?", u) : S("%s(...): No `render` method found on the returned component instance: you may have forgotten to define `render`.", u)), i.getInitialState && !i.getInitialState.isReactClassApproved && !i.state && S("getInitialState was defined on %s, a plain JavaScript class. This is only supported for classes created using React.createClass. Did you mean to define a state property instead?", u), i.getDefaultProps && !i.getDefaultProps.isReactClassApproved && S("getDefaultProps was defined on %s, a plain JavaScript class. This is only supported for classes created using React.createClass. Use a static property to define defaultProps instead.", u), i.propTypes && S("propTypes was defined as an instance property on %s. Use a static property to define propTypes instead.", u), i.contextType && S("contextType was defined as an instance property on %s. Use a static property to define contextType instead.", u), t.childContextTypes && !Ap.has(t) && // Strict Mode has its own warning for legacy context, so we can skip
        // this one.
        (e.mode & qt) === Ne && (Ap.add(t), S(`%s uses the legacy childContextTypes API which is no longer supported and will be removed in the next major release. Use React.createContext() instead

.Learn more about this warning here: https://reactjs.org/link/legacy-context`, u)), t.contextTypes && !Ap.has(t) && // Strict Mode has its own warning for legacy context, so we can skip
        // this one.
        (e.mode & qt) === Ne && (Ap.add(t), S(`%s uses the legacy contextTypes API which is no longer supported and will be removed in the next major release. Use React.createContext() with static contextType instead.

Learn more about this warning here: https://reactjs.org/link/legacy-context`, u)), i.contextTypes && S("contextTypes was defined as an instance property on %s. Use a static property to define contextTypes instead.", u), t.contextType && t.contextTypes && !fS.has(t) && (fS.add(t), S("%s declares both contextTypes and contextType static properties. The legacy contextTypes property will be ignored.", u)), typeof i.componentShouldUpdate == "function" && S("%s has a method called componentShouldUpdate(). Did you mean shouldComponentUpdate()? The name is phrased as a question because the function is expected to return a value.", u), t.prototype && t.prototype.isPureReactComponent && typeof i.shouldComponentUpdate < "u" && S("%s has a method called shouldComponentUpdate(). shouldComponentUpdate should not be used when extending React.PureComponent. Please extend React.Component if shouldComponentUpdate is used.", wt(t) || "A pure component"), typeof i.componentDidUnmount == "function" && S("%s has a method called componentDidUnmount(). But there is no such lifecycle method. Did you mean componentWillUnmount()?", u), typeof i.componentDidReceiveProps == "function" && S("%s has a method called componentDidReceiveProps(). But there is no such lifecycle method. If you meant to update the state in response to changing props, use componentWillReceiveProps(). If you meant to fetch data or run side-effects or mutations after React has updated the UI, use componentDidUpdate().", u), typeof i.componentWillRecieveProps == "function" && S("%s has a method called componentWillRecieveProps(). Did you mean componentWillReceiveProps()?", u), typeof i.UNSAFE_componentWillRecieveProps == "function" && S("%s has a method called UNSAFE_componentWillRecieveProps(). Did you mean UNSAFE_componentWillReceiveProps()?", u);
        var f = i.props !== a;
        i.props !== void 0 && f && S("%s(...): When calling super() in `%s`, make sure to pass up the same props that your component's constructor was passed.", u, u), i.defaultProps && S("Setting defaultProps as an instance property on %s is not supported and will be ignored. Instead, define defaultProps as a static property on %s.", u, u), typeof i.getSnapshotBeforeUpdate == "function" && typeof i.componentDidUpdate != "function" && !uS.has(t) && (uS.add(t), S("%s: getSnapshotBeforeUpdate() should be used with componentDidUpdate(). This component defines getSnapshotBeforeUpdate() only.", wt(t))), typeof i.getDerivedStateFromProps == "function" && S("%s: getDerivedStateFromProps() is defined as an instance method and will be ignored. Instead, declare it as a static method.", u), typeof i.getDerivedStateFromError == "function" && S("%s: getDerivedStateFromError() is defined as an instance method and will be ignored. Instead, declare it as a static method.", u), typeof t.getSnapshotBeforeUpdate == "function" && S("%s: getSnapshotBeforeUpdate() is defined as a static method and will be ignored. Instead, declare it as an instance method.", u);
        var p = i.state;
        p && (typeof p != "object" || lt(p)) && S("%s.state: must be set to an object or null", u), typeof i.getChildContext == "function" && typeof t.childContextTypes != "object" && S("%s.getChildContext(): childContextTypes must be defined in order to use getChildContext().", u);
      }
    }
    function d0(e, t) {
      t.updater = vS, e.stateNode = t, Cu(t, e), t._reactInternalInstance = aS;
    }
    function p0(e, t, a) {
      var i = !1, u = fi, s = fi, f = t.contextType;
      if ("contextType" in t) {
        var p = (
          // Allow null for conditional declaration
          f === null || f !== void 0 && f.$$typeof === _ && f._context === void 0
        );
        if (!p && !dS.has(t)) {
          dS.add(t);
          var v = "";
          f === void 0 ? v = " However, it is set to undefined. This can be caused by a typo or by mixing up named and default imports. This can also happen due to a circular dependency, so try moving the createContext() call to a separate file." : typeof f != "object" ? v = " However, it is set to a " + typeof f + "." : f.$$typeof === gi ? v = " Did you accidentally pass the Context.Provider instead?" : f._context !== void 0 ? v = " Did you accidentally pass the Context.Consumer instead?" : v = " However, it is set to an object with keys {" + Object.keys(f).join(", ") + "}.", S("%s defines an invalid contextType. contextType should point to the Context object returned by React.createContext().%s", wt(t) || "Component", v);
        }
      }
      if (typeof f == "object" && f !== null)
        s = rr(f);
      else {
        u = Df(e, t, !0);
        var y = t.contextTypes;
        i = y != null, s = i ? Of(e, u) : fi;
      }
      var g = new t(a, s);
      if (e.mode & qt) {
        gn(!0);
        try {
          g = new t(a, s);
        } finally {
          gn(!1);
        }
      }
      var x = e.memoizedState = g.state !== null && g.state !== void 0 ? g.state : null;
      d0(e, g);
      {
        if (typeof t.getDerivedStateFromProps == "function" && x === null) {
          var b = wt(t) || "Component";
          lS.has(b) || (lS.add(b), S("`%s` uses `getDerivedStateFromProps` but its initial state is %s. This is not recommended. Instead, define the initial state by assigning an object to `this.state` in the constructor of `%s`. This ensures that `getDerivedStateFromProps` arguments have a consistent shape.", b, g.state === null ? "null" : "undefined", b));
        }
        if (typeof t.getDerivedStateFromProps == "function" || typeof g.getSnapshotBeforeUpdate == "function") {
          var U = null, F = null, V = null;
          if (typeof g.componentWillMount == "function" && g.componentWillMount.__suppressDeprecationWarning !== !0 ? U = "componentWillMount" : typeof g.UNSAFE_componentWillMount == "function" && (U = "UNSAFE_componentWillMount"), typeof g.componentWillReceiveProps == "function" && g.componentWillReceiveProps.__suppressDeprecationWarning !== !0 ? F = "componentWillReceiveProps" : typeof g.UNSAFE_componentWillReceiveProps == "function" && (F = "UNSAFE_componentWillReceiveProps"), typeof g.componentWillUpdate == "function" && g.componentWillUpdate.__suppressDeprecationWarning !== !0 ? V = "componentWillUpdate" : typeof g.UNSAFE_componentWillUpdate == "function" && (V = "UNSAFE_componentWillUpdate"), U !== null || F !== null || V !== null) {
            var ce = wt(t) || "Component", Ue = typeof t.getDerivedStateFromProps == "function" ? "getDerivedStateFromProps()" : "getSnapshotBeforeUpdate()";
            oS.has(ce) || (oS.add(ce), S(`Unsafe legacy lifecycles will not be called for components using new component APIs.

%s uses %s but also contains the following legacy lifecycles:%s%s%s

The above lifecycles should be removed. Learn more about this warning here:
https://reactjs.org/link/unsafe-component-lifecycles`, ce, Ue, U !== null ? `
  ` + U : "", F !== null ? `
  ` + F : "", V !== null ? `
  ` + V : ""));
          }
        }
      }
      return i && nC(e, u, s), g;
    }
    function uw(e, t) {
      var a = t.state;
      typeof t.componentWillMount == "function" && t.componentWillMount(), typeof t.UNSAFE_componentWillMount == "function" && t.UNSAFE_componentWillMount(), a !== t.state && (S("%s.componentWillMount(): Assigning directly to this.state is deprecated (except inside a component's constructor). Use setState instead.", Qe(e) || "Component"), vS.enqueueReplaceState(t, t.state, null));
    }
    function v0(e, t, a, i) {
      var u = t.state;
      if (typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(a, i), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(a, i), t.state !== u) {
        {
          var s = Qe(e) || "Component";
          iS.has(s) || (iS.add(s), S("%s.componentWillReceiveProps(): Assigning directly to this.state is deprecated (except inside a component's constructor). Use setState instead.", s));
        }
        vS.enqueueReplaceState(t, t.state, null);
      }
    }
    function hS(e, t, a, i) {
      lw(e, t, a);
      var u = e.stateNode;
      u.props = a, u.state = e.memoizedState, u.refs = {}, Tg(e);
      var s = t.contextType;
      if (typeof s == "object" && s !== null)
        u.context = rr(s);
      else {
        var f = Df(e, t, !0);
        u.context = Of(e, f);
      }
      {
        if (u.state === a) {
          var p = wt(t) || "Component";
          cS.has(p) || (cS.add(p), S("%s: It is not recommended to assign props directly to state because updates to props won't be reflected in state. In most cases, it is better to use props directly.", p));
        }
        e.mode & qt && ol.recordLegacyContextWarning(e, u), ol.recordUnsafeLifecycleWarnings(e, u);
      }
      u.state = e.memoizedState;
      var v = t.getDerivedStateFromProps;
      if (typeof v == "function" && (pS(e, t, v, a), u.state = e.memoizedState), typeof t.getDerivedStateFromProps != "function" && typeof u.getSnapshotBeforeUpdate != "function" && (typeof u.UNSAFE_componentWillMount == "function" || typeof u.componentWillMount == "function") && (uw(e, u), um(e, a, u, i), u.state = e.memoizedState), typeof u.componentDidMount == "function") {
        var y = Ct;
        y |= Xi, (e.mode & Ut) !== Ne && (y |= Ul), e.flags |= y;
      }
    }
    function ow(e, t, a, i) {
      var u = e.stateNode, s = e.memoizedProps;
      u.props = s;
      var f = u.context, p = t.contextType, v = fi;
      if (typeof p == "object" && p !== null)
        v = rr(p);
      else {
        var y = Df(e, t, !0);
        v = Of(e, y);
      }
      var g = t.getDerivedStateFromProps, x = typeof g == "function" || typeof u.getSnapshotBeforeUpdate == "function";
      !x && (typeof u.UNSAFE_componentWillReceiveProps == "function" || typeof u.componentWillReceiveProps == "function") && (s !== a || f !== v) && v0(e, u, a, v), DC();
      var b = e.memoizedState, U = u.state = b;
      if (um(e, a, u, i), U = e.memoizedState, s === a && b === U && !Bh() && !om()) {
        if (typeof u.componentDidMount == "function") {
          var F = Ct;
          F |= Xi, (e.mode & Ut) !== Ne && (F |= Ul), e.flags |= F;
        }
        return !1;
      }
      typeof g == "function" && (pS(e, t, g, a), U = e.memoizedState);
      var V = om() || f0(e, t, s, a, b, U, v);
      if (V) {
        if (!x && (typeof u.UNSAFE_componentWillMount == "function" || typeof u.componentWillMount == "function") && (typeof u.componentWillMount == "function" && u.componentWillMount(), typeof u.UNSAFE_componentWillMount == "function" && u.UNSAFE_componentWillMount()), typeof u.componentDidMount == "function") {
          var ce = Ct;
          ce |= Xi, (e.mode & Ut) !== Ne && (ce |= Ul), e.flags |= ce;
        }
      } else {
        if (typeof u.componentDidMount == "function") {
          var Ue = Ct;
          Ue |= Xi, (e.mode & Ut) !== Ne && (Ue |= Ul), e.flags |= Ue;
        }
        e.memoizedProps = a, e.memoizedState = U;
      }
      return u.props = a, u.state = U, u.context = v, V;
    }
    function sw(e, t, a, i, u) {
      var s = t.stateNode;
      kC(e, t);
      var f = t.memoizedProps, p = t.type === t.elementType ? f : fl(t.type, f);
      s.props = p;
      var v = t.pendingProps, y = s.context, g = a.contextType, x = fi;
      if (typeof g == "object" && g !== null)
        x = rr(g);
      else {
        var b = Df(t, a, !0);
        x = Of(t, b);
      }
      var U = a.getDerivedStateFromProps, F = typeof U == "function" || typeof s.getSnapshotBeforeUpdate == "function";
      !F && (typeof s.UNSAFE_componentWillReceiveProps == "function" || typeof s.componentWillReceiveProps == "function") && (f !== v || y !== x) && v0(t, s, i, x), DC();
      var V = t.memoizedState, ce = s.state = V;
      if (um(t, i, s, u), ce = t.memoizedState, f === v && V === ce && !Bh() && !om() && !Te)
        return typeof s.componentDidUpdate == "function" && (f !== e.memoizedProps || V !== e.memoizedState) && (t.flags |= Ct), typeof s.getSnapshotBeforeUpdate == "function" && (f !== e.memoizedProps || V !== e.memoizedState) && (t.flags |= Wn), !1;
      typeof U == "function" && (pS(t, a, U, i), ce = t.memoizedState);
      var Ue = om() || f0(t, a, p, i, V, ce, x) || // TODO: In some cases, we'll end up checking if context has changed twice,
      // both before and after `shouldComponentUpdate` has been called. Not ideal,
      // but I'm loath to refactor this function. This only happens for memoized
      // components so it's not that common.
      Te;
      return Ue ? (!F && (typeof s.UNSAFE_componentWillUpdate == "function" || typeof s.componentWillUpdate == "function") && (typeof s.componentWillUpdate == "function" && s.componentWillUpdate(i, ce, x), typeof s.UNSAFE_componentWillUpdate == "function" && s.UNSAFE_componentWillUpdate(i, ce, x)), typeof s.componentDidUpdate == "function" && (t.flags |= Ct), typeof s.getSnapshotBeforeUpdate == "function" && (t.flags |= Wn)) : (typeof s.componentDidUpdate == "function" && (f !== e.memoizedProps || V !== e.memoizedState) && (t.flags |= Ct), typeof s.getSnapshotBeforeUpdate == "function" && (f !== e.memoizedProps || V !== e.memoizedState) && (t.flags |= Wn), t.memoizedProps = i, t.memoizedState = ce), s.props = i, s.state = ce, s.context = x, Ue;
    }
    function lc(e, t) {
      return {
        value: e,
        source: t,
        stack: Yi(t),
        digest: null
      };
    }
    function mS(e, t, a) {
      return {
        value: e,
        source: null,
        stack: a ?? null,
        digest: t ?? null
      };
    }
    function cw(e, t) {
      return !0;
    }
    function yS(e, t) {
      try {
        var a = cw(e, t);
        if (a === !1)
          return;
        var i = t.value, u = t.source, s = t.stack, f = s !== null ? s : "";
        if (i != null && i._suppressLogging) {
          if (e.tag === ne)
            return;
          console.error(i);
        }
        var p = u ? Qe(u) : null, v = p ? "The above error occurred in the <" + p + "> component:" : "The above error occurred in one of your React components:", y;
        if (e.tag === te)
          y = `Consider adding an error boundary to your tree to customize error handling behavior.
Visit https://reactjs.org/link/error-boundaries to learn more about error boundaries.`;
        else {
          var g = Qe(e) || "Anonymous";
          y = "React will try to recreate this component tree from scratch " + ("using the error boundary you provided, " + g + ".");
        }
        var x = v + `
` + f + `

` + ("" + y);
        console.error(x);
      } catch (b) {
        setTimeout(function() {
          throw b;
        });
      }
    }
    var fw = typeof WeakMap == "function" ? WeakMap : Map;
    function h0(e, t, a) {
      var i = Wu(Zt, a);
      i.tag = _g, i.payload = {
        element: null
      };
      var u = t.value;
      return i.callback = function() {
        rx(u), yS(e, t);
      }, i;
    }
    function gS(e, t, a) {
      var i = Wu(Zt, a);
      i.tag = _g;
      var u = e.type.getDerivedStateFromError;
      if (typeof u == "function") {
        var s = t.value;
        i.payload = function() {
          return u(s);
        }, i.callback = function() {
          w_(e), yS(e, t);
        };
      }
      var f = e.stateNode;
      return f !== null && typeof f.componentDidCatch == "function" && (i.callback = function() {
        w_(e), yS(e, t), typeof u != "function" && tx(this);
        var v = t.value, y = t.stack;
        this.componentDidCatch(v, {
          componentStack: y !== null ? y : ""
        }), typeof u != "function" && (na(e.lanes, Pe) || S("%s: Error boundaries should implement getDerivedStateFromError(). In that method, return a state update to display an error message or fallback UI.", Qe(e) || "Unknown"));
      }), i;
    }
    function m0(e, t, a) {
      var i = e.pingCache, u;
      if (i === null ? (i = e.pingCache = new fw(), u = /* @__PURE__ */ new Set(), i.set(t, u)) : (u = i.get(t), u === void 0 && (u = /* @__PURE__ */ new Set(), i.set(t, u))), !u.has(a)) {
        u.add(a);
        var s = ax.bind(null, e, t, a);
        ea && Jp(e, a), t.then(s, s);
      }
    }
    function dw(e, t, a, i) {
      var u = e.updateQueue;
      if (u === null) {
        var s = /* @__PURE__ */ new Set();
        s.add(a), e.updateQueue = s;
      } else
        u.add(a);
    }
    function pw(e, t) {
      var a = e.tag;
      if ((e.mode & ct) === Ne && (a === ee || a === Ke || a === Be)) {
        var i = e.alternate;
        i ? (e.updateQueue = i.updateQueue, e.memoizedState = i.memoizedState, e.lanes = i.lanes) : (e.updateQueue = null, e.memoizedState = null);
      }
    }
    function y0(e) {
      var t = e;
      do {
        if (t.tag === De && Wb(t))
          return t;
        t = t.return;
      } while (t !== null);
      return null;
    }
    function g0(e, t, a, i, u) {
      if ((e.mode & ct) === Ne) {
        if (e === t)
          e.flags |= Jn;
        else {
          if (e.flags |= xe, a.flags |= Nc, a.flags &= -52805, a.tag === ne) {
            var s = a.alternate;
            if (s === null)
              a.tag = Vt;
            else {
              var f = Wu(Zt, Pe);
              f.tag = rm, Po(a, f, Pe);
            }
          }
          a.lanes = et(a.lanes, Pe);
        }
        return e;
      }
      return e.flags |= Jn, e.lanes = u, e;
    }
    function vw(e, t, a, i, u) {
      if (a.flags |= hs, ea && Jp(e, u), i !== null && typeof i == "object" && typeof i.then == "function") {
        var s = i;
        pw(a), Fr() && a.mode & ct && sC();
        var f = y0(t);
        if (f !== null) {
          f.flags &= ~Rr, g0(f, t, a, e, u), f.mode & ct && m0(e, s, u), dw(f, e, s);
          return;
        } else {
          if (!Qv(u)) {
            m0(e, s, u), XS();
            return;
          }
          var p = new Error("A component suspended while responding to synchronous input. This will cause the UI to be replaced with a loading indicator. To fix, updates that suspend should be wrapped with startTransition.");
          i = p;
        }
      } else if (Fr() && a.mode & ct) {
        sC();
        var v = y0(t);
        if (v !== null) {
          (v.flags & Jn) === Oe && (v.flags |= Rr), g0(v, t, a, e, u), cg(lc(i, a));
          return;
        }
      }
      i = lc(i, a), W1(i);
      var y = t;
      do {
        switch (y.tag) {
          case te: {
            var g = i;
            y.flags |= Jn;
            var x = Os(u);
            y.lanes = et(y.lanes, x);
            var b = h0(y, g, x);
            bg(y, b);
            return;
          }
          case ne:
            var U = i, F = y.type, V = y.stateNode;
            if ((y.flags & xe) === Oe && (typeof F.getDerivedStateFromError == "function" || V !== null && typeof V.componentDidCatch == "function" && !y_(V))) {
              y.flags |= Jn;
              var ce = Os(u);
              y.lanes = et(y.lanes, ce);
              var Ue = gS(y, U, ce);
              bg(y, Ue);
              return;
            }
            break;
        }
        y = y.return;
      } while (y !== null);
    }
    function hw() {
      return null;
    }
    var jp = T.ReactCurrentOwner, dl = !1, SS, Fp, ES, CS, _S, uc, RS, Lm, Hp;
    SS = {}, Fp = {}, ES = {}, CS = {}, _S = {}, uc = !1, RS = {}, Lm = {}, Hp = {};
    function Ca(e, t, a, i) {
      e === null ? t.child = CC(t, null, a, i) : t.child = Uf(t, e.child, a, i);
    }
    function mw(e, t, a, i) {
      t.child = Uf(t, e.child, null, i), t.child = Uf(t, null, a, i);
    }
    function S0(e, t, a, i, u) {
      if (t.type !== t.elementType) {
        var s = a.propTypes;
        s && ll(
          s,
          i,
          // Resolved props
          "prop",
          wt(a)
        );
      }
      var f = a.render, p = t.ref, v, y;
      Af(t, u), ya(t);
      {
        if (jp.current = t, Qn(!0), v = Bf(e, t, f, i, p, u), y = $f(), t.mode & qt) {
          gn(!0);
          try {
            v = Bf(e, t, f, i, p, u), y = $f();
          } finally {
            gn(!1);
          }
        }
        Qn(!1);
      }
      return ga(), e !== null && !dl ? (zC(e, t, u), Gu(e, t, u)) : (Fr() && y && ag(t), t.flags |= li, Ca(e, t, v, u), t.child);
    }
    function E0(e, t, a, i, u) {
      if (e === null) {
        var s = a.type;
        if (Cx(s) && a.compare === null && // SimpleMemoComponent codepath doesn't resolve outer props either.
        a.defaultProps === void 0) {
          var f = s;
          return f = Xf(s), t.tag = Be, t.type = f, wS(t, s), C0(e, t, f, i, u);
        }
        {
          var p = s.propTypes;
          if (p && ll(
            p,
            i,
            // Resolved props
            "prop",
            wt(s)
          ), a.defaultProps !== void 0) {
            var v = wt(s) || "Unknown";
            Hp[v] || (S("%s: Support for defaultProps will be removed from memo components in a future major release. Use JavaScript default parameters instead.", v), Hp[v] = !0);
          }
        }
        var y = oE(a.type, null, i, t, t.mode, u);
        return y.ref = t.ref, y.return = t, t.child = y, y;
      }
      {
        var g = a.type, x = g.propTypes;
        x && ll(
          x,
          i,
          // Resolved props
          "prop",
          wt(g)
        );
      }
      var b = e.child, U = LS(e, u);
      if (!U) {
        var F = b.memoizedProps, V = a.compare;
        if (V = V !== null ? V : Ee, V(F, i) && e.ref === t.ref)
          return Gu(e, t, u);
      }
      t.flags |= li;
      var ce = dc(b, i);
      return ce.ref = t.ref, ce.return = t, t.child = ce, ce;
    }
    function C0(e, t, a, i, u) {
      if (t.type !== t.elementType) {
        var s = t.elementType;
        if (s.$$typeof === We) {
          var f = s, p = f._payload, v = f._init;
          try {
            s = v(p);
          } catch {
            s = null;
          }
          var y = s && s.propTypes;
          y && ll(
            y,
            i,
            // Resolved (SimpleMemoComponent has no defaultProps)
            "prop",
            wt(s)
          );
        }
      }
      if (e !== null) {
        var g = e.memoizedProps;
        if (Ee(g, i) && e.ref === t.ref && // Prevent bailout if the implementation changed due to hot reload.
        t.type === e.type)
          if (dl = !1, t.pendingProps = i = g, LS(e, u))
            (e.flags & Nc) !== Oe && (dl = !0);
          else return t.lanes = e.lanes, Gu(e, t, u);
      }
      return TS(e, t, a, i, u);
    }
    function _0(e, t, a) {
      var i = t.pendingProps, u = i.children, s = e !== null ? e.memoizedState : null;
      if (i.mode === "hidden" || ie)
        if ((t.mode & ct) === Ne) {
          var f = {
            baseLanes: Y,
            cachePool: null,
            transitions: null
          };
          t.memoizedState = f, Ym(t, a);
        } else if (na(a, ta)) {
          var x = {
            baseLanes: Y,
            cachePool: null,
            transitions: null
          };
          t.memoizedState = x;
          var b = s !== null ? s.baseLanes : a;
          Ym(t, b);
        } else {
          var p = null, v;
          if (s !== null) {
            var y = s.baseLanes;
            v = et(y, a);
          } else
            v = a;
          t.lanes = t.childLanes = ta;
          var g = {
            baseLanes: v,
            cachePool: p,
            transitions: null
          };
          return t.memoizedState = g, t.updateQueue = null, Ym(t, v), null;
        }
      else {
        var U;
        s !== null ? (U = et(s.baseLanes, a), t.memoizedState = null) : U = a, Ym(t, U);
      }
      return Ca(e, t, u, a), t.child;
    }
    function yw(e, t, a) {
      var i = t.pendingProps;
      return Ca(e, t, i, a), t.child;
    }
    function gw(e, t, a) {
      var i = t.pendingProps.children;
      return Ca(e, t, i, a), t.child;
    }
    function Sw(e, t, a) {
      {
        t.flags |= Ct;
        {
          var i = t.stateNode;
          i.effectDuration = 0, i.passiveEffectDuration = 0;
        }
      }
      var u = t.pendingProps, s = u.children;
      return Ca(e, t, s, a), t.child;
    }
    function R0(e, t) {
      var a = t.ref;
      (e === null && a !== null || e !== null && e.ref !== a) && (t.flags |= Cn, t.flags |= _o);
    }
    function TS(e, t, a, i, u) {
      if (t.type !== t.elementType) {
        var s = a.propTypes;
        s && ll(
          s,
          i,
          // Resolved props
          "prop",
          wt(a)
        );
      }
      var f;
      {
        var p = Df(t, a, !0);
        f = Of(t, p);
      }
      var v, y;
      Af(t, u), ya(t);
      {
        if (jp.current = t, Qn(!0), v = Bf(e, t, a, i, f, u), y = $f(), t.mode & qt) {
          gn(!0);
          try {
            v = Bf(e, t, a, i, f, u), y = $f();
          } finally {
            gn(!1);
          }
        }
        Qn(!1);
      }
      return ga(), e !== null && !dl ? (zC(e, t, u), Gu(e, t, u)) : (Fr() && y && ag(t), t.flags |= li, Ca(e, t, v, u), t.child);
    }
    function T0(e, t, a, i, u) {
      {
        switch (Ax(t)) {
          case !1: {
            var s = t.stateNode, f = t.type, p = new f(t.memoizedProps, s.context), v = p.state;
            s.updater.enqueueSetState(s, v, null);
            break;
          }
          case !0: {
            t.flags |= xe, t.flags |= Jn;
            var y = new Error("Simulated error coming from DevTools"), g = Os(u);
            t.lanes = et(t.lanes, g);
            var x = gS(t, lc(y, t), g);
            bg(t, x);
            break;
          }
        }
        if (t.type !== t.elementType) {
          var b = a.propTypes;
          b && ll(
            b,
            i,
            // Resolved props
            "prop",
            wt(a)
          );
        }
      }
      var U;
      Xl(a) ? (U = !0, Ih(t)) : U = !1, Af(t, u);
      var F = t.stateNode, V;
      F === null ? (Um(e, t), p0(t, a, i), hS(t, a, i, u), V = !0) : e === null ? V = ow(t, a, i, u) : V = sw(e, t, a, i, u);
      var ce = bS(e, t, a, V, U, u);
      {
        var Ue = t.stateNode;
        V && Ue.props !== i && (uc || S("It looks like %s is reassigning its own `this.props` while rendering. This is not supported and can lead to confusing bugs.", Qe(t) || "a component"), uc = !0);
      }
      return ce;
    }
    function bS(e, t, a, i, u, s) {
      R0(e, t);
      var f = (t.flags & xe) !== Oe;
      if (!i && !f)
        return u && iC(t, a, !1), Gu(e, t, s);
      var p = t.stateNode;
      jp.current = t;
      var v;
      if (f && typeof a.getDerivedStateFromError != "function")
        v = null, o0();
      else {
        ya(t);
        {
          if (Qn(!0), v = p.render(), t.mode & qt) {
            gn(!0);
            try {
              p.render();
            } finally {
              gn(!1);
            }
          }
          Qn(!1);
        }
        ga();
      }
      return t.flags |= li, e !== null && f ? mw(e, t, v, s) : Ca(e, t, v, s), t.memoizedState = p.state, u && iC(t, a, !0), t.child;
    }
    function b0(e) {
      var t = e.stateNode;
      t.pendingContext ? rC(e, t.pendingContext, t.pendingContext !== t.context) : t.context && rC(e, t.context, !1), wg(e, t.containerInfo);
    }
    function Ew(e, t, a) {
      if (b0(t), e === null)
        throw new Error("Should have a current fiber. This is a bug in React.");
      var i = t.pendingProps, u = t.memoizedState, s = u.element;
      kC(e, t), um(t, i, null, a);
      var f = t.memoizedState;
      t.stateNode;
      var p = f.element;
      if (u.isDehydrated) {
        var v = {
          element: p,
          isDehydrated: !1,
          cache: f.cache,
          pendingSuspenseBoundaries: f.pendingSuspenseBoundaries,
          transitions: f.transitions
        }, y = t.updateQueue;
        if (y.baseState = v, t.memoizedState = v, t.flags & Rr) {
          var g = lc(new Error("There was an error while hydrating. Because the error happened outside of a Suspense boundary, the entire root will switch to client rendering."), t);
          return w0(e, t, p, a, g);
        } else if (p !== s) {
          var x = lc(new Error("This root received an early update, before anything was able hydrate. Switched the entire root to client rendering."), t);
          return w0(e, t, p, a, x);
        } else {
          Rb(t);
          var b = CC(t, null, p, a);
          t.child = b;
          for (var U = b; U; )
            U.flags = U.flags & ~yn | Xr, U = U.sibling;
        }
      } else {
        if (Mf(), p === s)
          return Gu(e, t, a);
        Ca(e, t, p, a);
      }
      return t.child;
    }
    function w0(e, t, a, i, u) {
      return Mf(), cg(u), t.flags |= Rr, Ca(e, t, a, i), t.child;
    }
    function Cw(e, t, a) {
      LC(t), e === null && sg(t);
      var i = t.type, u = t.pendingProps, s = e !== null ? e.memoizedProps : null, f = u.children, p = Iy(i, u);
      return p ? f = null : s !== null && Iy(i, s) && (t.flags |= Ma), R0(e, t), Ca(e, t, f, a), t.child;
    }
    function _w(e, t) {
      return e === null && sg(t), null;
    }
    function Rw(e, t, a, i) {
      Um(e, t);
      var u = t.pendingProps, s = a, f = s._payload, p = s._init, v = p(f);
      t.type = v;
      var y = t.tag = _x(v), g = fl(v, u), x;
      switch (y) {
        case ee:
          return wS(t, v), t.type = v = Xf(v), x = TS(null, t, v, g, i), x;
        case ne:
          return t.type = v = nE(v), x = T0(null, t, v, g, i), x;
        case Ke:
          return t.type = v = rE(v), x = S0(null, t, v, g, i), x;
        case dt: {
          if (t.type !== t.elementType) {
            var b = v.propTypes;
            b && ll(
              b,
              g,
              // Resolved for outer only
              "prop",
              wt(v)
            );
          }
          return x = E0(
            null,
            t,
            v,
            fl(v.type, g),
            // The inner type can have defaults too
            i
          ), x;
        }
      }
      var U = "";
      throw v !== null && typeof v == "object" && v.$$typeof === We && (U = " Did you wrap a component in React.lazy() more than once?"), new Error("Element type is invalid. Received a promise that resolves to: " + v + ". " + ("Lazy element type must resolve to a class or function." + U));
    }
    function Tw(e, t, a, i, u) {
      Um(e, t), t.tag = ne;
      var s;
      return Xl(a) ? (s = !0, Ih(t)) : s = !1, Af(t, u), p0(t, a, i), hS(t, a, i, u), bS(null, t, a, !0, s, u);
    }
    function bw(e, t, a, i) {
      Um(e, t);
      var u = t.pendingProps, s;
      {
        var f = Df(t, a, !1);
        s = Of(t, f);
      }
      Af(t, i);
      var p, v;
      ya(t);
      {
        if (a.prototype && typeof a.prototype.render == "function") {
          var y = wt(a) || "Unknown";
          SS[y] || (S("The <%s /> component appears to have a render method, but doesn't extend React.Component. This is likely to cause errors. Change %s to extend React.Component instead.", y, y), SS[y] = !0);
        }
        t.mode & qt && ol.recordLegacyContextWarning(t, null), Qn(!0), jp.current = t, p = Bf(null, t, a, u, s, i), v = $f(), Qn(!1);
      }
      if (ga(), t.flags |= li, typeof p == "object" && p !== null && typeof p.render == "function" && p.$$typeof === void 0) {
        var g = wt(a) || "Unknown";
        Fp[g] || (S("The <%s /> component appears to be a function component that returns a class instance. Change %s to a class that extends React.Component instead. If you can't use a class try assigning the prototype on the function as a workaround. `%s.prototype = React.Component.prototype`. Don't use an arrow function since it cannot be called with `new` by React.", g, g, g), Fp[g] = !0);
      }
      if (
        // Run these checks in production only if the flag is off.
        // Eventually we'll delete this branch altogether.
        typeof p == "object" && p !== null && typeof p.render == "function" && p.$$typeof === void 0
      ) {
        {
          var x = wt(a) || "Unknown";
          Fp[x] || (S("The <%s /> component appears to be a function component that returns a class instance. Change %s to a class that extends React.Component instead. If you can't use a class try assigning the prototype on the function as a workaround. `%s.prototype = React.Component.prototype`. Don't use an arrow function since it cannot be called with `new` by React.", x, x, x), Fp[x] = !0);
        }
        t.tag = ne, t.memoizedState = null, t.updateQueue = null;
        var b = !1;
        return Xl(a) ? (b = !0, Ih(t)) : b = !1, t.memoizedState = p.state !== null && p.state !== void 0 ? p.state : null, Tg(t), d0(t, p), hS(t, a, u, i), bS(null, t, a, !0, b, i);
      } else {
        if (t.tag = ee, t.mode & qt) {
          gn(!0);
          try {
            p = Bf(null, t, a, u, s, i), v = $f();
          } finally {
            gn(!1);
          }
        }
        return Fr() && v && ag(t), Ca(null, t, p, i), wS(t, a), t.child;
      }
    }
    function wS(e, t) {
      {
        if (t && t.childContextTypes && S("%s(...): childContextTypes cannot be defined on a function component.", t.displayName || t.name || "Component"), e.ref !== null) {
          var a = "", i = Nr();
          i && (a += `

Check the render method of \`` + i + "`.");
          var u = i || "", s = e._debugSource;
          s && (u = s.fileName + ":" + s.lineNumber), _S[u] || (_S[u] = !0, S("Function components cannot be given refs. Attempts to access this ref will fail. Did you mean to use React.forwardRef()?%s", a));
        }
        if (t.defaultProps !== void 0) {
          var f = wt(t) || "Unknown";
          Hp[f] || (S("%s: Support for defaultProps will be removed from function components in a future major release. Use JavaScript default parameters instead.", f), Hp[f] = !0);
        }
        if (typeof t.getDerivedStateFromProps == "function") {
          var p = wt(t) || "Unknown";
          CS[p] || (S("%s: Function components do not support getDerivedStateFromProps.", p), CS[p] = !0);
        }
        if (typeof t.contextType == "object" && t.contextType !== null) {
          var v = wt(t) || "Unknown";
          ES[v] || (S("%s: Function components do not support contextType.", v), ES[v] = !0);
        }
      }
    }
    var xS = {
      dehydrated: null,
      treeContext: null,
      retryLane: Ot
    };
    function kS(e) {
      return {
        baseLanes: e,
        cachePool: hw(),
        transitions: null
      };
    }
    function ww(e, t) {
      var a = null;
      return {
        baseLanes: et(e.baseLanes, t),
        cachePool: a,
        transitions: e.transitions
      };
    }
    function xw(e, t, a, i) {
      if (t !== null) {
        var u = t.memoizedState;
        if (u === null)
          return !1;
      }
      return Dg(e, kp);
    }
    function kw(e, t) {
      return Ns(e.childLanes, t);
    }
    function x0(e, t, a) {
      var i = t.pendingProps;
      jx(t) && (t.flags |= xe);
      var u = sl.current, s = !1, f = (t.flags & xe) !== Oe;
      if (f || xw(u, e) ? (s = !0, t.flags &= ~xe) : (e === null || e.memoizedState !== null) && (u = Qb(u, UC)), u = Ff(u), $o(t, u), e === null) {
        sg(t);
        var p = t.memoizedState;
        if (p !== null) {
          var v = p.dehydrated;
          if (v !== null)
            return Mw(t, v);
        }
        var y = i.children, g = i.fallback;
        if (s) {
          var x = Dw(t, y, g, a), b = t.child;
          return b.memoizedState = kS(a), t.memoizedState = xS, x;
        } else
          return DS(t, y);
      } else {
        var U = e.memoizedState;
        if (U !== null) {
          var F = U.dehydrated;
          if (F !== null)
            return Uw(e, t, f, i, F, U, a);
        }
        if (s) {
          var V = i.fallback, ce = i.children, Ue = Nw(e, t, ce, V, a), we = t.child, Tt = e.child.memoizedState;
          return we.memoizedState = Tt === null ? kS(a) : ww(Tt, a), we.childLanes = kw(e, a), t.memoizedState = xS, Ue;
        } else {
          var gt = i.children, N = Ow(e, t, gt, a);
          return t.memoizedState = null, N;
        }
      }
    }
    function DS(e, t, a) {
      var i = e.mode, u = {
        mode: "visible",
        children: t
      }, s = OS(u, i);
      return s.return = e, e.child = s, s;
    }
    function Dw(e, t, a, i) {
      var u = e.mode, s = e.child, f = {
        mode: "hidden",
        children: t
      }, p, v;
      return (u & ct) === Ne && s !== null ? (p = s, p.childLanes = Y, p.pendingProps = f, e.mode & Mt && (p.actualDuration = 0, p.actualStartTime = -1, p.selfBaseDuration = 0, p.treeBaseDuration = 0), v = Xo(a, u, i, null)) : (p = OS(f, u), v = Xo(a, u, i, null)), p.return = e, v.return = e, p.sibling = v, e.child = p, v;
    }
    function OS(e, t, a) {
      return k_(e, t, Y, null);
    }
    function k0(e, t) {
      return dc(e, t);
    }
    function Ow(e, t, a, i) {
      var u = e.child, s = u.sibling, f = k0(u, {
        mode: "visible",
        children: a
      });
      if ((t.mode & ct) === Ne && (f.lanes = i), f.return = t, f.sibling = null, s !== null) {
        var p = t.deletions;
        p === null ? (t.deletions = [s], t.flags |= La) : p.push(s);
      }
      return t.child = f, f;
    }
    function Nw(e, t, a, i, u) {
      var s = t.mode, f = e.child, p = f.sibling, v = {
        mode: "hidden",
        children: a
      }, y;
      if (
        // In legacy mode, we commit the primary tree as if it successfully
        // completed, even though it's in an inconsistent state.
        (s & ct) === Ne && // Make sure we're on the second pass, i.e. the primary child fragment was
        // already cloned. In legacy mode, the only case where this isn't true is
        // when DevTools forces us to display a fallback; we skip the first render
        // pass entirely and go straight to rendering the fallback. (In Concurrent
        // Mode, SuspenseList can also trigger this scenario, but this is a legacy-
        // only codepath.)
        t.child !== f
      ) {
        var g = t.child;
        y = g, y.childLanes = Y, y.pendingProps = v, t.mode & Mt && (y.actualDuration = 0, y.actualStartTime = -1, y.selfBaseDuration = f.selfBaseDuration, y.treeBaseDuration = f.treeBaseDuration), t.deletions = null;
      } else
        y = k0(f, v), y.subtreeFlags = f.subtreeFlags & zn;
      var x;
      return p !== null ? x = dc(p, i) : (x = Xo(i, s, u, null), x.flags |= yn), x.return = t, y.return = t, y.sibling = x, t.child = y, x;
    }
    function Mm(e, t, a, i) {
      i !== null && cg(i), Uf(t, e.child, null, a);
      var u = t.pendingProps, s = u.children, f = DS(t, s);
      return f.flags |= yn, t.memoizedState = null, f;
    }
    function Lw(e, t, a, i, u) {
      var s = t.mode, f = {
        mode: "visible",
        children: a
      }, p = OS(f, s), v = Xo(i, s, u, null);
      return v.flags |= yn, p.return = t, v.return = t, p.sibling = v, t.child = p, (t.mode & ct) !== Ne && Uf(t, e.child, null, u), v;
    }
    function Mw(e, t, a) {
      return (e.mode & ct) === Ne ? (S("Cannot hydrate Suspense in legacy mode. Switch from ReactDOM.hydrate(element, container) to ReactDOMClient.hydrateRoot(container, <App />).render(element) or remove the Suspense components from the server rendered components."), e.lanes = Pe) : Gy(t) ? e.lanes = Tr : e.lanes = ta, null;
    }
    function Uw(e, t, a, i, u, s, f) {
      if (a)
        if (t.flags & Rr) {
          t.flags &= ~Rr;
          var N = mS(new Error("There was an error while hydrating this Suspense boundary. Switched to client rendering."));
          return Mm(e, t, f, N);
        } else {
          if (t.memoizedState !== null)
            return t.child = e.child, t.flags |= xe, null;
          var P = i.children, L = i.fallback, K = Lw(e, t, P, L, f), he = t.child;
          return he.memoizedState = kS(f), t.memoizedState = xS, K;
        }
      else {
        if (Cb(), (t.mode & ct) === Ne)
          return Mm(
            e,
            t,
            f,
            // TODO: When we delete legacy mode, we should make this error argument
            // required — every concurrent mode path that causes hydration to
            // de-opt to client rendering should have an error message.
            null
          );
        if (Gy(u)) {
          var p, v, y;
          {
            var g = FT(u);
            p = g.digest, v = g.message, y = g.stack;
          }
          var x;
          v ? x = new Error(v) : x = new Error("The server could not finish this Suspense boundary, likely due to an error during server rendering. Switched to client rendering.");
          var b = mS(x, p, y);
          return Mm(e, t, f, b);
        }
        var U = na(f, e.childLanes);
        if (dl || U) {
          var F = Im();
          if (F !== null) {
            var V = Bd(F, f);
            if (V !== Ot && V !== s.retryLane) {
              s.retryLane = V;
              var ce = Zt;
              Ba(e, V), Sr(F, e, V, ce);
            }
          }
          XS();
          var Ue = mS(new Error("This Suspense boundary received an update before it finished hydrating. This caused the boundary to switch to client rendering. The usual way to fix this is to wrap the original update in startTransition."));
          return Mm(e, t, f, Ue);
        } else if (XE(u)) {
          t.flags |= xe, t.child = e.child;
          var we = ix.bind(null, e);
          return HT(u, we), null;
        } else {
          Tb(t, u, s.treeContext);
          var Tt = i.children, gt = DS(t, Tt);
          return gt.flags |= Xr, gt;
        }
      }
    }
    function D0(e, t, a) {
      e.lanes = et(e.lanes, t);
      var i = e.alternate;
      i !== null && (i.lanes = et(i.lanes, t)), Eg(e.return, t, a);
    }
    function zw(e, t, a) {
      for (var i = t; i !== null; ) {
        if (i.tag === De) {
          var u = i.memoizedState;
          u !== null && D0(i, a, e);
        } else if (i.tag === un)
          D0(i, a, e);
        else if (i.child !== null) {
          i.child.return = i, i = i.child;
          continue;
        }
        if (i === e)
          return;
        for (; i.sibling === null; ) {
          if (i.return === null || i.return === e)
            return;
          i = i.return;
        }
        i.sibling.return = i.return, i = i.sibling;
      }
    }
    function Aw(e) {
      for (var t = e, a = null; t !== null; ) {
        var i = t.alternate;
        i !== null && fm(i) === null && (a = t), t = t.sibling;
      }
      return a;
    }
    function jw(e) {
      if (e !== void 0 && e !== "forwards" && e !== "backwards" && e !== "together" && !RS[e])
        if (RS[e] = !0, typeof e == "string")
          switch (e.toLowerCase()) {
            case "together":
            case "forwards":
            case "backwards": {
              S('"%s" is not a valid value for revealOrder on <SuspenseList />. Use lowercase "%s" instead.', e, e.toLowerCase());
              break;
            }
            case "forward":
            case "backward": {
              S('"%s" is not a valid value for revealOrder on <SuspenseList />. React uses the -s suffix in the spelling. Use "%ss" instead.', e, e.toLowerCase());
              break;
            }
            default:
              S('"%s" is not a supported revealOrder on <SuspenseList />. Did you mean "together", "forwards" or "backwards"?', e);
              break;
          }
        else
          S('%s is not a supported value for revealOrder on <SuspenseList />. Did you mean "together", "forwards" or "backwards"?', e);
    }
    function Fw(e, t) {
      e !== void 0 && !Lm[e] && (e !== "collapsed" && e !== "hidden" ? (Lm[e] = !0, S('"%s" is not a supported value for tail on <SuspenseList />. Did you mean "collapsed" or "hidden"?', e)) : t !== "forwards" && t !== "backwards" && (Lm[e] = !0, S('<SuspenseList tail="%s" /> is only valid if revealOrder is "forwards" or "backwards". Did you mean to specify revealOrder="forwards"?', e)));
    }
    function O0(e, t) {
      {
        var a = lt(e), i = !a && typeof Je(e) == "function";
        if (a || i) {
          var u = a ? "array" : "iterable";
          return S("A nested %s was passed to row #%s in <SuspenseList />. Wrap it in an additional SuspenseList to configure its revealOrder: <SuspenseList revealOrder=...> ... <SuspenseList revealOrder=...>{%s}</SuspenseList> ... </SuspenseList>", u, t, u), !1;
        }
      }
      return !0;
    }
    function Hw(e, t) {
      if ((t === "forwards" || t === "backwards") && e !== void 0 && e !== null && e !== !1)
        if (lt(e)) {
          for (var a = 0; a < e.length; a++)
            if (!O0(e[a], a))
              return;
        } else {
          var i = Je(e);
          if (typeof i == "function") {
            var u = i.call(e);
            if (u)
              for (var s = u.next(), f = 0; !s.done; s = u.next()) {
                if (!O0(s.value, f))
                  return;
                f++;
              }
          } else
            S('A single row was passed to a <SuspenseList revealOrder="%s" />. This is not useful since it needs multiple rows. Did you mean to pass multiple children or an array?', t);
        }
    }
    function NS(e, t, a, i, u) {
      var s = e.memoizedState;
      s === null ? e.memoizedState = {
        isBackwards: t,
        rendering: null,
        renderingStartTime: 0,
        last: i,
        tail: a,
        tailMode: u
      } : (s.isBackwards = t, s.rendering = null, s.renderingStartTime = 0, s.last = i, s.tail = a, s.tailMode = u);
    }
    function N0(e, t, a) {
      var i = t.pendingProps, u = i.revealOrder, s = i.tail, f = i.children;
      jw(u), Fw(s, u), Hw(f, u), Ca(e, t, f, a);
      var p = sl.current, v = Dg(p, kp);
      if (v)
        p = Og(p, kp), t.flags |= xe;
      else {
        var y = e !== null && (e.flags & xe) !== Oe;
        y && zw(t, t.child, a), p = Ff(p);
      }
      if ($o(t, p), (t.mode & ct) === Ne)
        t.memoizedState = null;
      else
        switch (u) {
          case "forwards": {
            var g = Aw(t.child), x;
            g === null ? (x = t.child, t.child = null) : (x = g.sibling, g.sibling = null), NS(
              t,
              !1,
              // isBackwards
              x,
              g,
              s
            );
            break;
          }
          case "backwards": {
            var b = null, U = t.child;
            for (t.child = null; U !== null; ) {
              var F = U.alternate;
              if (F !== null && fm(F) === null) {
                t.child = U;
                break;
              }
              var V = U.sibling;
              U.sibling = b, b = U, U = V;
            }
            NS(
              t,
              !0,
              // isBackwards
              b,
              null,
              // last
              s
            );
            break;
          }
          case "together": {
            NS(
              t,
              !1,
              // isBackwards
              null,
              // tail
              null,
              // last
              void 0
            );
            break;
          }
          default:
            t.memoizedState = null;
        }
      return t.child;
    }
    function Vw(e, t, a) {
      wg(t, t.stateNode.containerInfo);
      var i = t.pendingProps;
      return e === null ? t.child = Uf(t, null, i, a) : Ca(e, t, i, a), t.child;
    }
    var L0 = !1;
    function Pw(e, t, a) {
      var i = t.type, u = i._context, s = t.pendingProps, f = t.memoizedProps, p = s.value;
      {
        "value" in s || L0 || (L0 = !0, S("The `value` prop is required for the `<Context.Provider>`. Did you misspell it or forget to pass it?"));
        var v = t.type.propTypes;
        v && ll(v, s, "prop", "Context.Provider");
      }
      if (TC(t, u, p), f !== null) {
        var y = f.value;
        if (G(y, p)) {
          if (f.children === s.children && !Bh())
            return Gu(e, t, a);
        } else
          jb(t, u, a);
      }
      var g = s.children;
      return Ca(e, t, g, a), t.child;
    }
    var M0 = !1;
    function Bw(e, t, a) {
      var i = t.type;
      i._context === void 0 ? i !== i.Consumer && (M0 || (M0 = !0, S("Rendering <Context> directly is not supported and will be removed in a future major release. Did you mean to render <Context.Consumer> instead?"))) : i = i._context;
      var u = t.pendingProps, s = u.children;
      typeof s != "function" && S("A context consumer was rendered with multiple children, or a child that isn't a function. A context consumer expects a single child that is a function. If you did pass a function, make sure there is no trailing or leading whitespace around it."), Af(t, a);
      var f = rr(i);
      ya(t);
      var p;
      return jp.current = t, Qn(!0), p = s(f), Qn(!1), ga(), t.flags |= li, Ca(e, t, p, a), t.child;
    }
    function Vp() {
      dl = !0;
    }
    function Um(e, t) {
      (t.mode & ct) === Ne && e !== null && (e.alternate = null, t.alternate = null, t.flags |= yn);
    }
    function Gu(e, t, a) {
      return e !== null && (t.dependencies = e.dependencies), o0(), Zp(t.lanes), na(a, t.childLanes) ? (zb(e, t), t.child) : null;
    }
    function $w(e, t, a) {
      {
        var i = t.return;
        if (i === null)
          throw new Error("Cannot swap the root fiber.");
        if (e.alternate = null, t.alternate = null, a.index = t.index, a.sibling = t.sibling, a.return = t.return, a.ref = t.ref, t === i.child)
          i.child = a;
        else {
          var u = i.child;
          if (u === null)
            throw new Error("Expected parent to have a child.");
          for (; u.sibling !== t; )
            if (u = u.sibling, u === null)
              throw new Error("Expected to find the previous sibling.");
          u.sibling = a;
        }
        var s = i.deletions;
        return s === null ? (i.deletions = [e], i.flags |= La) : s.push(e), a.flags |= yn, a;
      }
    }
    function LS(e, t) {
      var a = e.lanes;
      return !!na(a, t);
    }
    function Iw(e, t, a) {
      switch (t.tag) {
        case te:
          b0(t), t.stateNode, Mf();
          break;
        case fe:
          LC(t);
          break;
        case ne: {
          var i = t.type;
          Xl(i) && Ih(t);
          break;
        }
        case me:
          wg(t, t.stateNode.containerInfo);
          break;
        case ht: {
          var u = t.memoizedProps.value, s = t.type._context;
          TC(t, s, u);
          break;
        }
        case yt:
          {
            var f = na(a, t.childLanes);
            f && (t.flags |= Ct);
            {
              var p = t.stateNode;
              p.effectDuration = 0, p.passiveEffectDuration = 0;
            }
          }
          break;
        case De: {
          var v = t.memoizedState;
          if (v !== null) {
            if (v.dehydrated !== null)
              return $o(t, Ff(sl.current)), t.flags |= xe, null;
            var y = t.child, g = y.childLanes;
            if (na(a, g))
              return x0(e, t, a);
            $o(t, Ff(sl.current));
            var x = Gu(e, t, a);
            return x !== null ? x.sibling : null;
          } else
            $o(t, Ff(sl.current));
          break;
        }
        case un: {
          var b = (e.flags & xe) !== Oe, U = na(a, t.childLanes);
          if (b) {
            if (U)
              return N0(e, t, a);
            t.flags |= xe;
          }
          var F = t.memoizedState;
          if (F !== null && (F.rendering = null, F.tail = null, F.lastEffect = null), $o(t, sl.current), U)
            break;
          return null;
        }
        case Le:
        case Ft:
          return t.lanes = Y, _0(e, t, a);
      }
      return Gu(e, t, a);
    }
    function U0(e, t, a) {
      if (t._debugNeedsRemount && e !== null)
        return $w(e, t, oE(t.type, t.key, t.pendingProps, t._debugOwner || null, t.mode, t.lanes));
      if (e !== null) {
        var i = e.memoizedProps, u = t.pendingProps;
        if (i !== u || Bh() || // Force a re-render if the implementation changed due to hot reload:
        t.type !== e.type)
          dl = !0;
        else {
          var s = LS(e, a);
          if (!s && // If this is the second pass of an error or suspense boundary, there
          // may not be work scheduled on `current`, so we check for this flag.
          (t.flags & xe) === Oe)
            return dl = !1, Iw(e, t, a);
          (e.flags & Nc) !== Oe ? dl = !0 : dl = !1;
        }
      } else if (dl = !1, Fr() && hb(t)) {
        var f = t.index, p = mb();
        oC(t, p, f);
      }
      switch (t.lanes = Y, t.tag) {
        case Ve:
          return bw(e, t, t.type, a);
        case ln: {
          var v = t.elementType;
          return Rw(e, t, v, a);
        }
        case ee: {
          var y = t.type, g = t.pendingProps, x = t.elementType === y ? g : fl(y, g);
          return TS(e, t, y, x, a);
        }
        case ne: {
          var b = t.type, U = t.pendingProps, F = t.elementType === b ? U : fl(b, U);
          return T0(e, t, b, F, a);
        }
        case te:
          return Ew(e, t, a);
        case fe:
          return Cw(e, t, a);
        case qe:
          return _w(e, t);
        case De:
          return x0(e, t, a);
        case me:
          return Vw(e, t, a);
        case Ke: {
          var V = t.type, ce = t.pendingProps, Ue = t.elementType === V ? ce : fl(V, ce);
          return S0(e, t, V, Ue, a);
        }
        case Et:
          return yw(e, t, a);
        case mt:
          return gw(e, t, a);
        case yt:
          return Sw(e, t, a);
        case ht:
          return Pw(e, t, a);
        case dn:
          return Bw(e, t, a);
        case dt: {
          var we = t.type, Tt = t.pendingProps, gt = fl(we, Tt);
          if (t.type !== t.elementType) {
            var N = we.propTypes;
            N && ll(
              N,
              gt,
              // Resolved for outer only
              "prop",
              wt(we)
            );
          }
          return gt = fl(we.type, gt), E0(e, t, we, gt, a);
        }
        case Be:
          return C0(e, t, t.type, t.pendingProps, a);
        case Vt: {
          var P = t.type, L = t.pendingProps, K = t.elementType === P ? L : fl(P, L);
          return Tw(e, t, P, K, a);
        }
        case un:
          return N0(e, t, a);
        case kt:
          break;
        case Le:
          return _0(e, t, a);
      }
      throw new Error("Unknown unit of work tag (" + t.tag + "). This error is likely caused by a bug in React. Please file an issue.");
    }
    function If(e) {
      e.flags |= Ct;
    }
    function z0(e) {
      e.flags |= Cn, e.flags |= _o;
    }
    var A0, MS, j0, F0;
    A0 = function(e, t, a, i) {
      for (var u = t.child; u !== null; ) {
        if (u.tag === fe || u.tag === qe)
          dT(e, u.stateNode);
        else if (u.tag !== me) {
          if (u.child !== null) {
            u.child.return = u, u = u.child;
            continue;
          }
        }
        if (u === t)
          return;
        for (; u.sibling === null; ) {
          if (u.return === null || u.return === t)
            return;
          u = u.return;
        }
        u.sibling.return = u.return, u = u.sibling;
      }
    }, MS = function(e, t) {
    }, j0 = function(e, t, a, i, u) {
      var s = e.memoizedProps;
      if (s !== i) {
        var f = t.stateNode, p = xg(), v = vT(f, a, s, i, u, p);
        t.updateQueue = v, v && If(t);
      }
    }, F0 = function(e, t, a, i) {
      a !== i && If(t);
    };
    function Pp(e, t) {
      if (!Fr())
        switch (e.tailMode) {
          case "hidden": {
            for (var a = e.tail, i = null; a !== null; )
              a.alternate !== null && (i = a), a = a.sibling;
            i === null ? e.tail = null : i.sibling = null;
            break;
          }
          case "collapsed": {
            for (var u = e.tail, s = null; u !== null; )
              u.alternate !== null && (s = u), u = u.sibling;
            s === null ? !t && e.tail !== null ? e.tail.sibling = null : e.tail = null : s.sibling = null;
            break;
          }
        }
    }
    function Vr(e) {
      var t = e.alternate !== null && e.alternate.child === e.child, a = Y, i = Oe;
      if (t) {
        if ((e.mode & Mt) !== Ne) {
          for (var v = e.selfBaseDuration, y = e.child; y !== null; )
            a = et(a, et(y.lanes, y.childLanes)), i |= y.subtreeFlags & zn, i |= y.flags & zn, v += y.treeBaseDuration, y = y.sibling;
          e.treeBaseDuration = v;
        } else
          for (var g = e.child; g !== null; )
            a = et(a, et(g.lanes, g.childLanes)), i |= g.subtreeFlags & zn, i |= g.flags & zn, g.return = e, g = g.sibling;
        e.subtreeFlags |= i;
      } else {
        if ((e.mode & Mt) !== Ne) {
          for (var u = e.actualDuration, s = e.selfBaseDuration, f = e.child; f !== null; )
            a = et(a, et(f.lanes, f.childLanes)), i |= f.subtreeFlags, i |= f.flags, u += f.actualDuration, s += f.treeBaseDuration, f = f.sibling;
          e.actualDuration = u, e.treeBaseDuration = s;
        } else
          for (var p = e.child; p !== null; )
            a = et(a, et(p.lanes, p.childLanes)), i |= p.subtreeFlags, i |= p.flags, p.return = e, p = p.sibling;
        e.subtreeFlags |= i;
      }
      return e.childLanes = a, t;
    }
    function Yw(e, t, a) {
      if (Db() && (t.mode & ct) !== Ne && (t.flags & xe) === Oe)
        return hC(t), Mf(), t.flags |= Rr | hs | Jn, !1;
      var i = qh(t);
      if (a !== null && a.dehydrated !== null)
        if (e === null) {
          if (!i)
            throw new Error("A dehydrated suspense component was completed without a hydrated node. This is probably a bug in React.");
          if (xb(t), Vr(t), (t.mode & Mt) !== Ne) {
            var u = a !== null;
            if (u) {
              var s = t.child;
              s !== null && (t.treeBaseDuration -= s.treeBaseDuration);
            }
          }
          return !1;
        } else {
          if (Mf(), (t.flags & xe) === Oe && (t.memoizedState = null), t.flags |= Ct, Vr(t), (t.mode & Mt) !== Ne) {
            var f = a !== null;
            if (f) {
              var p = t.child;
              p !== null && (t.treeBaseDuration -= p.treeBaseDuration);
            }
          }
          return !1;
        }
      else
        return mC(), !0;
    }
    function H0(e, t, a) {
      var i = t.pendingProps;
      switch (ig(t), t.tag) {
        case Ve:
        case ln:
        case Be:
        case ee:
        case Ke:
        case Et:
        case mt:
        case yt:
        case dn:
        case dt:
          return Vr(t), null;
        case ne: {
          var u = t.type;
          return Xl(u) && $h(t), Vr(t), null;
        }
        case te: {
          var s = t.stateNode;
          if (jf(t), tg(t), Lg(), s.pendingContext && (s.context = s.pendingContext, s.pendingContext = null), e === null || e.child === null) {
            var f = qh(t);
            if (f)
              If(t);
            else if (e !== null) {
              var p = e.memoizedState;
              // Check if this is a client root
              (!p.isDehydrated || // Check if we reverted to client rendering (e.g. due to an error)
              (t.flags & Rr) !== Oe) && (t.flags |= Wn, mC());
            }
          }
          return MS(e, t), Vr(t), null;
        }
        case fe: {
          kg(t);
          var v = NC(), y = t.type;
          if (e !== null && t.stateNode != null)
            j0(e, t, y, i, v), e.ref !== t.ref && z0(t);
          else {
            if (!i) {
              if (t.stateNode === null)
                throw new Error("We must have new props for new mounts. This error is likely caused by a bug in React. Please file an issue.");
              return Vr(t), null;
            }
            var g = xg(), x = qh(t);
            if (x)
              bb(t, v, g) && If(t);
            else {
              var b = fT(y, i, v, g, t);
              A0(b, t, !1, !1), t.stateNode = b, pT(b, y, i, v) && If(t);
            }
            t.ref !== null && z0(t);
          }
          return Vr(t), null;
        }
        case qe: {
          var U = i;
          if (e && t.stateNode != null) {
            var F = e.memoizedProps;
            F0(e, t, F, U);
          } else {
            if (typeof U != "string" && t.stateNode === null)
              throw new Error("We must have new props for new mounts. This error is likely caused by a bug in React. Please file an issue.");
            var V = NC(), ce = xg(), Ue = qh(t);
            Ue ? wb(t) && If(t) : t.stateNode = hT(U, V, ce, t);
          }
          return Vr(t), null;
        }
        case De: {
          Hf(t);
          var we = t.memoizedState;
          if (e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
            var Tt = Yw(e, t, we);
            if (!Tt)
              return t.flags & Jn ? t : null;
          }
          if ((t.flags & xe) !== Oe)
            return t.lanes = a, (t.mode & Mt) !== Ne && rS(t), t;
          var gt = we !== null, N = e !== null && e.memoizedState !== null;
          if (gt !== N && gt) {
            var P = t.child;
            if (P.flags |= Un, (t.mode & ct) !== Ne) {
              var L = e === null && (t.memoizedProps.unstable_avoidThisFallback !== !0 || !0);
              L || Dg(sl.current, UC) ? Q1() : XS();
            }
          }
          var K = t.updateQueue;
          if (K !== null && (t.flags |= Ct), Vr(t), (t.mode & Mt) !== Ne && gt) {
            var he = t.child;
            he !== null && (t.treeBaseDuration -= he.treeBaseDuration);
          }
          return null;
        }
        case me:
          return jf(t), MS(e, t), e === null && ob(t.stateNode.containerInfo), Vr(t), null;
        case ht:
          var de = t.type._context;
          return Sg(de, t), Vr(t), null;
        case Vt: {
          var Ie = t.type;
          return Xl(Ie) && $h(t), Vr(t), null;
        }
        case un: {
          Hf(t);
          var Xe = t.memoizedState;
          if (Xe === null)
            return Vr(t), null;
          var Xt = (t.flags & xe) !== Oe, At = Xe.rendering;
          if (At === null)
            if (Xt)
              Pp(Xe, !1);
            else {
              var Kn = G1() && (e === null || (e.flags & xe) === Oe);
              if (!Kn)
                for (var jt = t.child; jt !== null; ) {
                  var Pn = fm(jt);
                  if (Pn !== null) {
                    Xt = !0, t.flags |= xe, Pp(Xe, !1);
                    var sa = Pn.updateQueue;
                    return sa !== null && (t.updateQueue = sa, t.flags |= Ct), t.subtreeFlags = Oe, Ab(t, a), $o(t, Og(sl.current, kp)), t.child;
                  }
                  jt = jt.sibling;
                }
              Xe.tail !== null && Gn() > l_() && (t.flags |= xe, Xt = !0, Pp(Xe, !1), t.lanes = Md);
            }
          else {
            if (!Xt) {
              var Yr = fm(At);
              if (Yr !== null) {
                t.flags |= xe, Xt = !0;
                var pi = Yr.updateQueue;
                if (pi !== null && (t.updateQueue = pi, t.flags |= Ct), Pp(Xe, !0), Xe.tail === null && Xe.tailMode === "hidden" && !At.alternate && !Fr())
                  return Vr(t), null;
              } else // The time it took to render last row is greater than the remaining
              // time we have to render. So rendering one more row would likely
              // exceed it.
              Gn() * 2 - Xe.renderingStartTime > l_() && a !== ta && (t.flags |= xe, Xt = !0, Pp(Xe, !1), t.lanes = Md);
            }
            if (Xe.isBackwards)
              At.sibling = t.child, t.child = At;
            else {
              var Ta = Xe.last;
              Ta !== null ? Ta.sibling = At : t.child = At, Xe.last = At;
            }
          }
          if (Xe.tail !== null) {
            var ba = Xe.tail;
            Xe.rendering = ba, Xe.tail = ba.sibling, Xe.renderingStartTime = Gn(), ba.sibling = null;
            var ca = sl.current;
            return Xt ? ca = Og(ca, kp) : ca = Ff(ca), $o(t, ca), ba;
          }
          return Vr(t), null;
        }
        case kt:
          break;
        case Le:
        case Ft: {
          KS(t);
          var Ju = t.memoizedState, Zf = Ju !== null;
          if (e !== null) {
            var rv = e.memoizedState, iu = rv !== null;
            iu !== Zf && // LegacyHidden doesn't do any hiding — it only pre-renders.
            !ie && (t.flags |= Un);
          }
          return !Zf || (t.mode & ct) === Ne ? Vr(t) : na(au, ta) && (Vr(t), t.subtreeFlags & (yn | Ct) && (t.flags |= Un)), null;
        }
        case Dt:
          return null;
        case Nt:
          return null;
      }
      throw new Error("Unknown unit of work tag (" + t.tag + "). This error is likely caused by a bug in React. Please file an issue.");
    }
    function Qw(e, t, a) {
      switch (ig(t), t.tag) {
        case ne: {
          var i = t.type;
          Xl(i) && $h(t);
          var u = t.flags;
          return u & Jn ? (t.flags = u & ~Jn | xe, (t.mode & Mt) !== Ne && rS(t), t) : null;
        }
        case te: {
          t.stateNode, jf(t), tg(t), Lg();
          var s = t.flags;
          return (s & Jn) !== Oe && (s & xe) === Oe ? (t.flags = s & ~Jn | xe, t) : null;
        }
        case fe:
          return kg(t), null;
        case De: {
          Hf(t);
          var f = t.memoizedState;
          if (f !== null && f.dehydrated !== null) {
            if (t.alternate === null)
              throw new Error("Threw in newly mounted dehydrated component. This is likely a bug in React. Please file an issue.");
            Mf();
          }
          var p = t.flags;
          return p & Jn ? (t.flags = p & ~Jn | xe, (t.mode & Mt) !== Ne && rS(t), t) : null;
        }
        case un:
          return Hf(t), null;
        case me:
          return jf(t), null;
        case ht:
          var v = t.type._context;
          return Sg(v, t), null;
        case Le:
        case Ft:
          return KS(t), null;
        case Dt:
          return null;
        default:
          return null;
      }
    }
    function V0(e, t, a) {
      switch (ig(t), t.tag) {
        case ne: {
          var i = t.type.childContextTypes;
          i != null && $h(t);
          break;
        }
        case te: {
          t.stateNode, jf(t), tg(t), Lg();
          break;
        }
        case fe: {
          kg(t);
          break;
        }
        case me:
          jf(t);
          break;
        case De:
          Hf(t);
          break;
        case un:
          Hf(t);
          break;
        case ht:
          var u = t.type._context;
          Sg(u, t);
          break;
        case Le:
        case Ft:
          KS(t);
          break;
      }
    }
    var P0 = null;
    P0 = /* @__PURE__ */ new Set();
    var zm = !1, Pr = !1, Ww = typeof WeakSet == "function" ? WeakSet : Set, Ce = null, Yf = null, Qf = null;
    function Gw(e) {
      Ml(null, function() {
        throw e;
      }), vs();
    }
    var qw = function(e, t) {
      if (t.props = e.memoizedProps, t.state = e.memoizedState, e.mode & Mt)
        try {
          nu(), t.componentWillUnmount();
        } finally {
          tu(e);
        }
      else
        t.componentWillUnmount();
    };
    function B0(e, t) {
      try {
        Qo(pr, e);
      } catch (a) {
        fn(e, t, a);
      }
    }
    function US(e, t, a) {
      try {
        qw(e, a);
      } catch (i) {
        fn(e, t, i);
      }
    }
    function Kw(e, t, a) {
      try {
        a.componentDidMount();
      } catch (i) {
        fn(e, t, i);
      }
    }
    function $0(e, t) {
      try {
        Y0(e);
      } catch (a) {
        fn(e, t, a);
      }
    }
    function Wf(e, t) {
      var a = e.ref;
      if (a !== null)
        if (typeof a == "function") {
          var i;
          try {
            if (Fe && ut && e.mode & Mt)
              try {
                nu(), i = a(null);
              } finally {
                tu(e);
              }
            else
              i = a(null);
          } catch (u) {
            fn(e, t, u);
          }
          typeof i == "function" && S("Unexpected return value from a callback ref in %s. A callback ref should not return a function.", Qe(e));
        } else
          a.current = null;
    }
    function Am(e, t, a) {
      try {
        a();
      } catch (i) {
        fn(e, t, i);
      }
    }
    var I0 = !1;
    function Xw(e, t) {
      sT(e.containerInfo), Ce = t, Zw();
      var a = I0;
      return I0 = !1, a;
    }
    function Zw() {
      for (; Ce !== null; ) {
        var e = Ce, t = e.child;
        (e.subtreeFlags & zl) !== Oe && t !== null ? (t.return = e, Ce = t) : Jw();
      }
    }
    function Jw() {
      for (; Ce !== null; ) {
        var e = Ce;
        Qt(e);
        try {
          e1(e);
        } catch (a) {
          fn(e, e.return, a);
        }
        cn();
        var t = e.sibling;
        if (t !== null) {
          t.return = e.return, Ce = t;
          return;
        }
        Ce = e.return;
      }
    }
    function e1(e) {
      var t = e.alternate, a = e.flags;
      if ((a & Wn) !== Oe) {
        switch (Qt(e), e.tag) {
          case ee:
          case Ke:
          case Be:
            break;
          case ne: {
            if (t !== null) {
              var i = t.memoizedProps, u = t.memoizedState, s = e.stateNode;
              e.type === e.elementType && !uc && (s.props !== e.memoizedProps && S("Expected %s props to match memoized props before getSnapshotBeforeUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", Qe(e) || "instance"), s.state !== e.memoizedState && S("Expected %s state to match memoized state before getSnapshotBeforeUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", Qe(e) || "instance"));
              var f = s.getSnapshotBeforeUpdate(e.elementType === e.type ? i : fl(e.type, i), u);
              {
                var p = P0;
                f === void 0 && !p.has(e.type) && (p.add(e.type), S("%s.getSnapshotBeforeUpdate(): A snapshot value (or null) must be returned. You have returned undefined.", Qe(e)));
              }
              s.__reactInternalSnapshotBeforeUpdate = f;
            }
            break;
          }
          case te: {
            {
              var v = e.stateNode;
              UT(v.containerInfo);
            }
            break;
          }
          case fe:
          case qe:
          case me:
          case Vt:
            break;
          default:
            throw new Error("This unit of work tag should not have side-effects. This error is likely caused by a bug in React. Please file an issue.");
        }
        cn();
      }
    }
    function pl(e, t, a) {
      var i = t.updateQueue, u = i !== null ? i.lastEffect : null;
      if (u !== null) {
        var s = u.next, f = s;
        do {
          if ((f.tag & e) === e) {
            var p = f.destroy;
            f.destroy = void 0, p !== void 0 && ((e & Hr) !== $a ? el(t) : (e & pr) !== $a && ys(t), (e & Zl) !== $a && ev(!0), Am(t, a, p), (e & Zl) !== $a && ev(!1), (e & Hr) !== $a ? Hl() : (e & pr) !== $a && Nd());
          }
          f = f.next;
        } while (f !== s);
      }
    }
    function Qo(e, t) {
      var a = t.updateQueue, i = a !== null ? a.lastEffect : null;
      if (i !== null) {
        var u = i.next, s = u;
        do {
          if ((s.tag & e) === e) {
            (e & Hr) !== $a ? Od(t) : (e & pr) !== $a && jc(t);
            var f = s.create;
            (e & Zl) !== $a && ev(!0), s.destroy = f(), (e & Zl) !== $a && ev(!1), (e & Hr) !== $a ? Pv() : (e & pr) !== $a && Bv();
            {
              var p = s.destroy;
              if (p !== void 0 && typeof p != "function") {
                var v = void 0;
                (s.tag & pr) !== Oe ? v = "useLayoutEffect" : (s.tag & Zl) !== Oe ? v = "useInsertionEffect" : v = "useEffect";
                var y = void 0;
                p === null ? y = " You returned null. If your effect does not require clean up, return undefined (or nothing)." : typeof p.then == "function" ? y = `

It looks like you wrote ` + v + `(async () => ...) or returned a Promise. Instead, write the async function inside your effect and call it immediately:

` + v + `(() => {
  async function fetchData() {
    // You can await here
    const response = await MyAPI.getData(someId);
    // ...
  }
  fetchData();
}, [someId]); // Or [] if effect doesn't need props or state

Learn more about data fetching with Hooks: https://reactjs.org/link/hooks-data-fetching` : y = " You returned: " + p, S("%s must not return anything besides a function, which is used for clean-up.%s", v, y);
              }
            }
          }
          s = s.next;
        } while (s !== u);
      }
    }
    function t1(e, t) {
      if ((t.flags & Ct) !== Oe)
        switch (t.tag) {
          case yt: {
            var a = t.stateNode.passiveEffectDuration, i = t.memoizedProps, u = i.id, s = i.onPostCommit, f = l0(), p = t.alternate === null ? "mount" : "update";
            i0() && (p = "nested-update"), typeof s == "function" && s(u, p, a, f);
            var v = t.return;
            e: for (; v !== null; ) {
              switch (v.tag) {
                case te:
                  var y = v.stateNode;
                  y.passiveEffectDuration += a;
                  break e;
                case yt:
                  var g = v.stateNode;
                  g.passiveEffectDuration += a;
                  break e;
              }
              v = v.return;
            }
            break;
          }
        }
    }
    function n1(e, t, a, i) {
      if ((a.flags & jl) !== Oe)
        switch (a.tag) {
          case ee:
          case Ke:
          case Be: {
            if (!Pr)
              if (a.mode & Mt)
                try {
                  nu(), Qo(pr | dr, a);
                } finally {
                  tu(a);
                }
              else
                Qo(pr | dr, a);
            break;
          }
          case ne: {
            var u = a.stateNode;
            if (a.flags & Ct && !Pr)
              if (t === null)
                if (a.type === a.elementType && !uc && (u.props !== a.memoizedProps && S("Expected %s props to match memoized props before componentDidMount. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", Qe(a) || "instance"), u.state !== a.memoizedState && S("Expected %s state to match memoized state before componentDidMount. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", Qe(a) || "instance")), a.mode & Mt)
                  try {
                    nu(), u.componentDidMount();
                  } finally {
                    tu(a);
                  }
                else
                  u.componentDidMount();
              else {
                var s = a.elementType === a.type ? t.memoizedProps : fl(a.type, t.memoizedProps), f = t.memoizedState;
                if (a.type === a.elementType && !uc && (u.props !== a.memoizedProps && S("Expected %s props to match memoized props before componentDidUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", Qe(a) || "instance"), u.state !== a.memoizedState && S("Expected %s state to match memoized state before componentDidUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", Qe(a) || "instance")), a.mode & Mt)
                  try {
                    nu(), u.componentDidUpdate(s, f, u.__reactInternalSnapshotBeforeUpdate);
                  } finally {
                    tu(a);
                  }
                else
                  u.componentDidUpdate(s, f, u.__reactInternalSnapshotBeforeUpdate);
              }
            var p = a.updateQueue;
            p !== null && (a.type === a.elementType && !uc && (u.props !== a.memoizedProps && S("Expected %s props to match memoized props before processing the update queue. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", Qe(a) || "instance"), u.state !== a.memoizedState && S("Expected %s state to match memoized state before processing the update queue. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", Qe(a) || "instance")), OC(a, p, u));
            break;
          }
          case te: {
            var v = a.updateQueue;
            if (v !== null) {
              var y = null;
              if (a.child !== null)
                switch (a.child.tag) {
                  case fe:
                    y = a.child.stateNode;
                    break;
                  case ne:
                    y = a.child.stateNode;
                    break;
                }
              OC(a, v, y);
            }
            break;
          }
          case fe: {
            var g = a.stateNode;
            if (t === null && a.flags & Ct) {
              var x = a.type, b = a.memoizedProps;
              ET(g, x, b);
            }
            break;
          }
          case qe:
            break;
          case me:
            break;
          case yt: {
            {
              var U = a.memoizedProps, F = U.onCommit, V = U.onRender, ce = a.stateNode.effectDuration, Ue = l0(), we = t === null ? "mount" : "update";
              i0() && (we = "nested-update"), typeof V == "function" && V(a.memoizedProps.id, we, a.actualDuration, a.treeBaseDuration, a.actualStartTime, Ue);
              {
                typeof F == "function" && F(a.memoizedProps.id, we, ce, Ue), J1(a);
                var Tt = a.return;
                e: for (; Tt !== null; ) {
                  switch (Tt.tag) {
                    case te:
                      var gt = Tt.stateNode;
                      gt.effectDuration += ce;
                      break e;
                    case yt:
                      var N = Tt.stateNode;
                      N.effectDuration += ce;
                      break e;
                  }
                  Tt = Tt.return;
                }
              }
            }
            break;
          }
          case De: {
            c1(e, a);
            break;
          }
          case un:
          case Vt:
          case kt:
          case Le:
          case Ft:
          case Nt:
            break;
          default:
            throw new Error("This unit of work tag should not have side-effects. This error is likely caused by a bug in React. Please file an issue.");
        }
      Pr || a.flags & Cn && Y0(a);
    }
    function r1(e) {
      switch (e.tag) {
        case ee:
        case Ke:
        case Be: {
          if (e.mode & Mt)
            try {
              nu(), B0(e, e.return);
            } finally {
              tu(e);
            }
          else
            B0(e, e.return);
          break;
        }
        case ne: {
          var t = e.stateNode;
          typeof t.componentDidMount == "function" && Kw(e, e.return, t), $0(e, e.return);
          break;
        }
        case fe: {
          $0(e, e.return);
          break;
        }
      }
    }
    function a1(e, t) {
      for (var a = null, i = e; ; ) {
        if (i.tag === fe) {
          if (a === null) {
            a = i;
            try {
              var u = i.stateNode;
              t ? OT(u) : LT(i.stateNode, i.memoizedProps);
            } catch (f) {
              fn(e, e.return, f);
            }
          }
        } else if (i.tag === qe) {
          if (a === null)
            try {
              var s = i.stateNode;
              t ? NT(s) : MT(s, i.memoizedProps);
            } catch (f) {
              fn(e, e.return, f);
            }
        } else if (!((i.tag === Le || i.tag === Ft) && i.memoizedState !== null && i !== e)) {
          if (i.child !== null) {
            i.child.return = i, i = i.child;
            continue;
          }
        }
        if (i === e)
          return;
        for (; i.sibling === null; ) {
          if (i.return === null || i.return === e)
            return;
          a === i && (a = null), i = i.return;
        }
        a === i && (a = null), i.sibling.return = i.return, i = i.sibling;
      }
    }
    function Y0(e) {
      var t = e.ref;
      if (t !== null) {
        var a = e.stateNode, i;
        switch (e.tag) {
          case fe:
            i = a;
            break;
          default:
            i = a;
        }
        if (typeof t == "function") {
          var u;
          if (e.mode & Mt)
            try {
              nu(), u = t(i);
            } finally {
              tu(e);
            }
          else
            u = t(i);
          typeof u == "function" && S("Unexpected return value from a callback ref in %s. A callback ref should not return a function.", Qe(e));
        } else
          t.hasOwnProperty("current") || S("Unexpected ref object provided for %s. Use either a ref-setter function or React.createRef().", Qe(e)), t.current = i;
      }
    }
    function i1(e) {
      var t = e.alternate;
      t !== null && (t.return = null), e.return = null;
    }
    function Q0(e) {
      var t = e.alternate;
      t !== null && (e.alternate = null, Q0(t));
      {
        if (e.child = null, e.deletions = null, e.sibling = null, e.tag === fe) {
          var a = e.stateNode;
          a !== null && fb(a);
        }
        e.stateNode = null, e._debugOwner = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
      }
    }
    function l1(e) {
      for (var t = e.return; t !== null; ) {
        if (W0(t))
          return t;
        t = t.return;
      }
      throw new Error("Expected to find a host parent. This error is likely caused by a bug in React. Please file an issue.");
    }
    function W0(e) {
      return e.tag === fe || e.tag === te || e.tag === me;
    }
    function G0(e) {
      var t = e;
      e: for (; ; ) {
        for (; t.sibling === null; ) {
          if (t.return === null || W0(t.return))
            return null;
          t = t.return;
        }
        for (t.sibling.return = t.return, t = t.sibling; t.tag !== fe && t.tag !== qe && t.tag !== Jt; ) {
          if (t.flags & yn || t.child === null || t.tag === me)
            continue e;
          t.child.return = t, t = t.child;
        }
        if (!(t.flags & yn))
          return t.stateNode;
      }
    }
    function u1(e) {
      var t = l1(e);
      switch (t.tag) {
        case fe: {
          var a = t.stateNode;
          t.flags & Ma && (KE(a), t.flags &= ~Ma);
          var i = G0(e);
          AS(e, i, a);
          break;
        }
        case te:
        case me: {
          var u = t.stateNode.containerInfo, s = G0(e);
          zS(e, s, u);
          break;
        }
        default:
          throw new Error("Invalid host parent fiber. This error is likely caused by a bug in React. Please file an issue.");
      }
    }
    function zS(e, t, a) {
      var i = e.tag, u = i === fe || i === qe;
      if (u) {
        var s = e.stateNode;
        t ? wT(a, s, t) : TT(a, s);
      } else if (i !== me) {
        var f = e.child;
        if (f !== null) {
          zS(f, t, a);
          for (var p = f.sibling; p !== null; )
            zS(p, t, a), p = p.sibling;
        }
      }
    }
    function AS(e, t, a) {
      var i = e.tag, u = i === fe || i === qe;
      if (u) {
        var s = e.stateNode;
        t ? bT(a, s, t) : RT(a, s);
      } else if (i !== me) {
        var f = e.child;
        if (f !== null) {
          AS(f, t, a);
          for (var p = f.sibling; p !== null; )
            AS(p, t, a), p = p.sibling;
        }
      }
    }
    var Br = null, vl = !1;
    function o1(e, t, a) {
      {
        var i = t;
        e: for (; i !== null; ) {
          switch (i.tag) {
            case fe: {
              Br = i.stateNode, vl = !1;
              break e;
            }
            case te: {
              Br = i.stateNode.containerInfo, vl = !0;
              break e;
            }
            case me: {
              Br = i.stateNode.containerInfo, vl = !0;
              break e;
            }
          }
          i = i.return;
        }
        if (Br === null)
          throw new Error("Expected to find a host parent. This error is likely caused by a bug in React. Please file an issue.");
        q0(e, t, a), Br = null, vl = !1;
      }
      i1(a);
    }
    function Wo(e, t, a) {
      for (var i = a.child; i !== null; )
        q0(e, t, i), i = i.sibling;
    }
    function q0(e, t, a) {
      switch (xd(a), a.tag) {
        case fe:
          Pr || Wf(a, t);
        case qe: {
          {
            var i = Br, u = vl;
            Br = null, Wo(e, t, a), Br = i, vl = u, Br !== null && (vl ? kT(Br, a.stateNode) : xT(Br, a.stateNode));
          }
          return;
        }
        case Jt: {
          Br !== null && (vl ? DT(Br, a.stateNode) : Wy(Br, a.stateNode));
          return;
        }
        case me: {
          {
            var s = Br, f = vl;
            Br = a.stateNode.containerInfo, vl = !0, Wo(e, t, a), Br = s, vl = f;
          }
          return;
        }
        case ee:
        case Ke:
        case dt:
        case Be: {
          if (!Pr) {
            var p = a.updateQueue;
            if (p !== null) {
              var v = p.lastEffect;
              if (v !== null) {
                var y = v.next, g = y;
                do {
                  var x = g, b = x.destroy, U = x.tag;
                  b !== void 0 && ((U & Zl) !== $a ? Am(a, t, b) : (U & pr) !== $a && (ys(a), a.mode & Mt ? (nu(), Am(a, t, b), tu(a)) : Am(a, t, b), Nd())), g = g.next;
                } while (g !== y);
              }
            }
          }
          Wo(e, t, a);
          return;
        }
        case ne: {
          if (!Pr) {
            Wf(a, t);
            var F = a.stateNode;
            typeof F.componentWillUnmount == "function" && US(a, t, F);
          }
          Wo(e, t, a);
          return;
        }
        case kt: {
          Wo(e, t, a);
          return;
        }
        case Le: {
          if (
            // TODO: Remove this dead flag
            a.mode & ct
          ) {
            var V = Pr;
            Pr = V || a.memoizedState !== null, Wo(e, t, a), Pr = V;
          } else
            Wo(e, t, a);
          break;
        }
        default: {
          Wo(e, t, a);
          return;
        }
      }
    }
    function s1(e) {
      e.memoizedState;
    }
    function c1(e, t) {
      var a = t.memoizedState;
      if (a === null) {
        var i = t.alternate;
        if (i !== null) {
          var u = i.memoizedState;
          if (u !== null) {
            var s = u.dehydrated;
            s !== null && GT(s);
          }
        }
      }
    }
    function K0(e) {
      var t = e.updateQueue;
      if (t !== null) {
        e.updateQueue = null;
        var a = e.stateNode;
        a === null && (a = e.stateNode = new Ww()), t.forEach(function(i) {
          var u = lx.bind(null, e, i);
          if (!a.has(i)) {
            if (a.add(i), ea)
              if (Yf !== null && Qf !== null)
                Jp(Qf, Yf);
              else
                throw Error("Expected finished root and lanes to be set. This is a bug in React.");
            i.then(u, u);
          }
        });
      }
    }
    function f1(e, t, a) {
      Yf = a, Qf = e, Qt(t), X0(t, e), Qt(t), Yf = null, Qf = null;
    }
    function hl(e, t, a) {
      var i = t.deletions;
      if (i !== null)
        for (var u = 0; u < i.length; u++) {
          var s = i[u];
          try {
            o1(e, t, s);
          } catch (v) {
            fn(s, t, v);
          }
        }
      var f = wl();
      if (t.subtreeFlags & Al)
        for (var p = t.child; p !== null; )
          Qt(p), X0(p, e), p = p.sibling;
      Qt(f);
    }
    function X0(e, t, a) {
      var i = e.alternate, u = e.flags;
      switch (e.tag) {
        case ee:
        case Ke:
        case dt:
        case Be: {
          if (hl(t, e), ru(e), u & Ct) {
            try {
              pl(Zl | dr, e, e.return), Qo(Zl | dr, e);
            } catch (Ie) {
              fn(e, e.return, Ie);
            }
            if (e.mode & Mt) {
              try {
                nu(), pl(pr | dr, e, e.return);
              } catch (Ie) {
                fn(e, e.return, Ie);
              }
              tu(e);
            } else
              try {
                pl(pr | dr, e, e.return);
              } catch (Ie) {
                fn(e, e.return, Ie);
              }
          }
          return;
        }
        case ne: {
          hl(t, e), ru(e), u & Cn && i !== null && Wf(i, i.return);
          return;
        }
        case fe: {
          hl(t, e), ru(e), u & Cn && i !== null && Wf(i, i.return);
          {
            if (e.flags & Ma) {
              var s = e.stateNode;
              try {
                KE(s);
              } catch (Ie) {
                fn(e, e.return, Ie);
              }
            }
            if (u & Ct) {
              var f = e.stateNode;
              if (f != null) {
                var p = e.memoizedProps, v = i !== null ? i.memoizedProps : p, y = e.type, g = e.updateQueue;
                if (e.updateQueue = null, g !== null)
                  try {
                    CT(f, g, y, v, p, e);
                  } catch (Ie) {
                    fn(e, e.return, Ie);
                  }
              }
            }
          }
          return;
        }
        case qe: {
          if (hl(t, e), ru(e), u & Ct) {
            if (e.stateNode === null)
              throw new Error("This should have a text node initialized. This error is likely caused by a bug in React. Please file an issue.");
            var x = e.stateNode, b = e.memoizedProps, U = i !== null ? i.memoizedProps : b;
            try {
              _T(x, U, b);
            } catch (Ie) {
              fn(e, e.return, Ie);
            }
          }
          return;
        }
        case te: {
          if (hl(t, e), ru(e), u & Ct && i !== null) {
            var F = i.memoizedState;
            if (F.isDehydrated)
              try {
                WT(t.containerInfo);
              } catch (Ie) {
                fn(e, e.return, Ie);
              }
          }
          return;
        }
        case me: {
          hl(t, e), ru(e);
          return;
        }
        case De: {
          hl(t, e), ru(e);
          var V = e.child;
          if (V.flags & Un) {
            var ce = V.stateNode, Ue = V.memoizedState, we = Ue !== null;
            if (ce.isHidden = we, we) {
              var Tt = V.alternate !== null && V.alternate.memoizedState !== null;
              Tt || Y1();
            }
          }
          if (u & Ct) {
            try {
              s1(e);
            } catch (Ie) {
              fn(e, e.return, Ie);
            }
            K0(e);
          }
          return;
        }
        case Le: {
          var gt = i !== null && i.memoizedState !== null;
          if (
            // TODO: Remove this dead flag
            e.mode & ct
          ) {
            var N = Pr;
            Pr = N || gt, hl(t, e), Pr = N;
          } else
            hl(t, e);
          if (ru(e), u & Un) {
            var P = e.stateNode, L = e.memoizedState, K = L !== null, he = e;
            if (P.isHidden = K, K && !gt && (he.mode & ct) !== Ne) {
              Ce = he;
              for (var de = he.child; de !== null; )
                Ce = de, p1(de), de = de.sibling;
            }
            a1(he, K);
          }
          return;
        }
        case un: {
          hl(t, e), ru(e), u & Ct && K0(e);
          return;
        }
        case kt:
          return;
        default: {
          hl(t, e), ru(e);
          return;
        }
      }
    }
    function ru(e) {
      var t = e.flags;
      if (t & yn) {
        try {
          u1(e);
        } catch (a) {
          fn(e, e.return, a);
        }
        e.flags &= ~yn;
      }
      t & Xr && (e.flags &= ~Xr);
    }
    function d1(e, t, a) {
      Yf = a, Qf = t, Ce = e, Z0(e, t, a), Yf = null, Qf = null;
    }
    function Z0(e, t, a) {
      for (var i = (e.mode & ct) !== Ne; Ce !== null; ) {
        var u = Ce, s = u.child;
        if (u.tag === Le && i) {
          var f = u.memoizedState !== null, p = f || zm;
          if (p) {
            jS(e, t, a);
            continue;
          } else {
            var v = u.alternate, y = v !== null && v.memoizedState !== null, g = y || Pr, x = zm, b = Pr;
            zm = p, Pr = g, Pr && !b && (Ce = u, v1(u));
            for (var U = s; U !== null; )
              Ce = U, Z0(
                U,
                // New root; bubble back up to here and stop.
                t,
                a
              ), U = U.sibling;
            Ce = u, zm = x, Pr = b, jS(e, t, a);
            continue;
          }
        }
        (u.subtreeFlags & jl) !== Oe && s !== null ? (s.return = u, Ce = s) : jS(e, t, a);
      }
    }
    function jS(e, t, a) {
      for (; Ce !== null; ) {
        var i = Ce;
        if ((i.flags & jl) !== Oe) {
          var u = i.alternate;
          Qt(i);
          try {
            n1(t, u, i, a);
          } catch (f) {
            fn(i, i.return, f);
          }
          cn();
        }
        if (i === e) {
          Ce = null;
          return;
        }
        var s = i.sibling;
        if (s !== null) {
          s.return = i.return, Ce = s;
          return;
        }
        Ce = i.return;
      }
    }
    function p1(e) {
      for (; Ce !== null; ) {
        var t = Ce, a = t.child;
        switch (t.tag) {
          case ee:
          case Ke:
          case dt:
          case Be: {
            if (t.mode & Mt)
              try {
                nu(), pl(pr, t, t.return);
              } finally {
                tu(t);
              }
            else
              pl(pr, t, t.return);
            break;
          }
          case ne: {
            Wf(t, t.return);
            var i = t.stateNode;
            typeof i.componentWillUnmount == "function" && US(t, t.return, i);
            break;
          }
          case fe: {
            Wf(t, t.return);
            break;
          }
          case Le: {
            var u = t.memoizedState !== null;
            if (u) {
              J0(e);
              continue;
            }
            break;
          }
        }
        a !== null ? (a.return = t, Ce = a) : J0(e);
      }
    }
    function J0(e) {
      for (; Ce !== null; ) {
        var t = Ce;
        if (t === e) {
          Ce = null;
          return;
        }
        var a = t.sibling;
        if (a !== null) {
          a.return = t.return, Ce = a;
          return;
        }
        Ce = t.return;
      }
    }
    function v1(e) {
      for (; Ce !== null; ) {
        var t = Ce, a = t.child;
        if (t.tag === Le) {
          var i = t.memoizedState !== null;
          if (i) {
            e_(e);
            continue;
          }
        }
        a !== null ? (a.return = t, Ce = a) : e_(e);
      }
    }
    function e_(e) {
      for (; Ce !== null; ) {
        var t = Ce;
        Qt(t);
        try {
          r1(t);
        } catch (i) {
          fn(t, t.return, i);
        }
        if (cn(), t === e) {
          Ce = null;
          return;
        }
        var a = t.sibling;
        if (a !== null) {
          a.return = t.return, Ce = a;
          return;
        }
        Ce = t.return;
      }
    }
    function h1(e, t, a, i) {
      Ce = t, m1(t, e, a, i);
    }
    function m1(e, t, a, i) {
      for (; Ce !== null; ) {
        var u = Ce, s = u.child;
        (u.subtreeFlags & Zi) !== Oe && s !== null ? (s.return = u, Ce = s) : y1(e, t, a, i);
      }
    }
    function y1(e, t, a, i) {
      for (; Ce !== null; ) {
        var u = Ce;
        if ((u.flags & Kr) !== Oe) {
          Qt(u);
          try {
            g1(t, u, a, i);
          } catch (f) {
            fn(u, u.return, f);
          }
          cn();
        }
        if (u === e) {
          Ce = null;
          return;
        }
        var s = u.sibling;
        if (s !== null) {
          s.return = u.return, Ce = s;
          return;
        }
        Ce = u.return;
      }
    }
    function g1(e, t, a, i) {
      switch (t.tag) {
        case ee:
        case Ke:
        case Be: {
          if (t.mode & Mt) {
            nS();
            try {
              Qo(Hr | dr, t);
            } finally {
              tS(t);
            }
          } else
            Qo(Hr | dr, t);
          break;
        }
      }
    }
    function S1(e) {
      Ce = e, E1();
    }
    function E1() {
      for (; Ce !== null; ) {
        var e = Ce, t = e.child;
        if ((Ce.flags & La) !== Oe) {
          var a = e.deletions;
          if (a !== null) {
            for (var i = 0; i < a.length; i++) {
              var u = a[i];
              Ce = u, R1(u, e);
            }
            {
              var s = e.alternate;
              if (s !== null) {
                var f = s.child;
                if (f !== null) {
                  s.child = null;
                  do {
                    var p = f.sibling;
                    f.sibling = null, f = p;
                  } while (f !== null);
                }
              }
            }
            Ce = e;
          }
        }
        (e.subtreeFlags & Zi) !== Oe && t !== null ? (t.return = e, Ce = t) : C1();
      }
    }
    function C1() {
      for (; Ce !== null; ) {
        var e = Ce;
        (e.flags & Kr) !== Oe && (Qt(e), _1(e), cn());
        var t = e.sibling;
        if (t !== null) {
          t.return = e.return, Ce = t;
          return;
        }
        Ce = e.return;
      }
    }
    function _1(e) {
      switch (e.tag) {
        case ee:
        case Ke:
        case Be: {
          e.mode & Mt ? (nS(), pl(Hr | dr, e, e.return), tS(e)) : pl(Hr | dr, e, e.return);
          break;
        }
      }
    }
    function R1(e, t) {
      for (; Ce !== null; ) {
        var a = Ce;
        Qt(a), b1(a, t), cn();
        var i = a.child;
        i !== null ? (i.return = a, Ce = i) : T1(e);
      }
    }
    function T1(e) {
      for (; Ce !== null; ) {
        var t = Ce, a = t.sibling, i = t.return;
        if (Q0(t), t === e) {
          Ce = null;
          return;
        }
        if (a !== null) {
          a.return = i, Ce = a;
          return;
        }
        Ce = i;
      }
    }
    function b1(e, t) {
      switch (e.tag) {
        case ee:
        case Ke:
        case Be: {
          e.mode & Mt ? (nS(), pl(Hr, e, t), tS(e)) : pl(Hr, e, t);
          break;
        }
      }
    }
    function w1(e) {
      switch (e.tag) {
        case ee:
        case Ke:
        case Be: {
          try {
            Qo(pr | dr, e);
          } catch (a) {
            fn(e, e.return, a);
          }
          break;
        }
        case ne: {
          var t = e.stateNode;
          try {
            t.componentDidMount();
          } catch (a) {
            fn(e, e.return, a);
          }
          break;
        }
      }
    }
    function x1(e) {
      switch (e.tag) {
        case ee:
        case Ke:
        case Be: {
          try {
            Qo(Hr | dr, e);
          } catch (t) {
            fn(e, e.return, t);
          }
          break;
        }
      }
    }
    function k1(e) {
      switch (e.tag) {
        case ee:
        case Ke:
        case Be: {
          try {
            pl(pr | dr, e, e.return);
          } catch (a) {
            fn(e, e.return, a);
          }
          break;
        }
        case ne: {
          var t = e.stateNode;
          typeof t.componentWillUnmount == "function" && US(e, e.return, t);
          break;
        }
      }
    }
    function D1(e) {
      switch (e.tag) {
        case ee:
        case Ke:
        case Be:
          try {
            pl(Hr | dr, e, e.return);
          } catch (t) {
            fn(e, e.return, t);
          }
      }
    }
    if (typeof Symbol == "function" && Symbol.for) {
      var Bp = Symbol.for;
      Bp("selector.component"), Bp("selector.has_pseudo_class"), Bp("selector.role"), Bp("selector.test_id"), Bp("selector.text");
    }
    var O1 = [];
    function N1() {
      O1.forEach(function(e) {
        return e();
      });
    }
    var L1 = T.ReactCurrentActQueue;
    function M1(e) {
      {
        var t = (
          // $FlowExpectedError – Flow doesn't know about IS_REACT_ACT_ENVIRONMENT global
          typeof IS_REACT_ACT_ENVIRONMENT < "u" ? IS_REACT_ACT_ENVIRONMENT : void 0
        ), a = typeof jest < "u";
        return a && t !== !1;
      }
    }
    function t_() {
      {
        var e = (
          // $FlowExpectedError – Flow doesn't know about IS_REACT_ACT_ENVIRONMENT global
          typeof IS_REACT_ACT_ENVIRONMENT < "u" ? IS_REACT_ACT_ENVIRONMENT : void 0
        );
        return !e && L1.current !== null && S("The current testing environment is not configured to support act(...)"), e;
      }
    }
    var U1 = Math.ceil, FS = T.ReactCurrentDispatcher, HS = T.ReactCurrentOwner, $r = T.ReactCurrentBatchConfig, ml = T.ReactCurrentActQueue, mr = (
      /*             */
      0
    ), n_ = (
      /*               */
      1
    ), Ir = (
      /*                */
      2
    ), Pi = (
      /*                */
      4
    ), qu = 0, $p = 1, oc = 2, jm = 3, Ip = 4, r_ = 5, VS = 6, Rt = mr, _a = null, On = null, yr = Y, au = Y, PS = jo(Y), gr = qu, Yp = null, Fm = Y, Qp = Y, Hm = Y, Wp = null, Ia = null, BS = 0, a_ = 500, i_ = 1 / 0, z1 = 500, Ku = null;
    function Gp() {
      i_ = Gn() + z1;
    }
    function l_() {
      return i_;
    }
    var Vm = !1, $S = null, Gf = null, sc = !1, Go = null, qp = Y, IS = [], YS = null, A1 = 50, Kp = 0, QS = null, WS = !1, Pm = !1, j1 = 50, qf = 0, Bm = null, Xp = Zt, $m = Y, u_ = !1;
    function Im() {
      return _a;
    }
    function Ra() {
      return (Rt & (Ir | Pi)) !== mr ? Gn() : (Xp !== Zt || (Xp = Gn()), Xp);
    }
    function qo(e) {
      var t = e.mode;
      if ((t & ct) === Ne)
        return Pe;
      if ((Rt & Ir) !== mr && yr !== Y)
        return Os(yr);
      var a = Lb() !== Nb;
      if (a) {
        if ($r.transition !== null) {
          var i = $r.transition;
          i._updatedFibers || (i._updatedFibers = /* @__PURE__ */ new Set()), i._updatedFibers.add(e);
        }
        return $m === Ot && ($m = Hd()), $m;
      }
      var u = Ha();
      if (u !== Ot)
        return u;
      var s = mT();
      return s;
    }
    function F1(e) {
      var t = e.mode;
      return (t & ct) === Ne ? Pe : Gv();
    }
    function Sr(e, t, a, i) {
      ox(), u_ && S("useInsertionEffect must not schedule updates."), WS && (Pm = !0), wo(e, a, i), (Rt & Ir) !== Y && e === _a ? fx(t) : (ea && Ms(e, t, a), dx(t), e === _a && ((Rt & Ir) === mr && (Qp = et(Qp, a)), gr === Ip && Ko(e, yr)), Ya(e, i), a === Pe && Rt === mr && (t.mode & ct) === Ne && // Treat `act` as if it's inside `batchedUpdates`, even in legacy mode.
      !ml.isBatchingLegacy && (Gp(), uC()));
    }
    function H1(e, t, a) {
      var i = e.current;
      i.lanes = t, wo(e, t, a), Ya(e, a);
    }
    function V1(e) {
      return (
        // TODO: Remove outdated deferRenderPhaseUpdateToNextBatch experiment. We
        // decided not to enable it.
        (Rt & Ir) !== mr
      );
    }
    function Ya(e, t) {
      var a = e.callbackNode;
      rf(e, t);
      var i = nf(e, e === _a ? yr : Y);
      if (i === Y) {
        a !== null && R_(a), e.callbackNode = null, e.callbackPriority = Ot;
        return;
      }
      var u = Bl(i), s = e.callbackPriority;
      if (s === u && // Special case related to `act`. If the currently scheduled task is a
      // Scheduler task, rather than an `act` task, cancel it and re-scheduled
      // on the `act` queue.
      !(ml.current !== null && a !== eE)) {
        a == null && s !== Pe && S("Expected scheduled callback to exist. This error is likely caused by a bug in React. Please file an issue.");
        return;
      }
      a != null && R_(a);
      var f;
      if (u === Pe)
        e.tag === Fo ? (ml.isBatchingLegacy !== null && (ml.didScheduleLegacyUpdate = !0), vb(c_.bind(null, e))) : lC(c_.bind(null, e)), ml.current !== null ? ml.current.push(Ho) : gT(function() {
          (Rt & (Ir | Pi)) === mr && Ho();
        }), f = null;
      else {
        var p;
        switch (th(i)) {
          case Mr:
            p = ms;
            break;
          case Ni:
            p = Fl;
            break;
          case ja:
            p = Ji;
            break;
          case Fa:
            p = Ru;
            break;
          default:
            p = Ji;
            break;
        }
        f = tE(p, o_.bind(null, e));
      }
      e.callbackPriority = u, e.callbackNode = f;
    }
    function o_(e, t) {
      if (aw(), Xp = Zt, $m = Y, (Rt & (Ir | Pi)) !== mr)
        throw new Error("Should not already be working.");
      var a = e.callbackNode, i = Zu();
      if (i && e.callbackNode !== a)
        return null;
      var u = nf(e, e === _a ? yr : Y);
      if (u === Y)
        return null;
      var s = !lf(e, u) && !Wv(e, u) && !t, f = s ? K1(e, u) : Qm(e, u);
      if (f !== qu) {
        if (f === oc) {
          var p = af(e);
          p !== Y && (u = p, f = GS(e, p));
        }
        if (f === $p) {
          var v = Yp;
          throw cc(e, Y), Ko(e, u), Ya(e, Gn()), v;
        }
        if (f === VS)
          Ko(e, u);
        else {
          var y = !lf(e, u), g = e.current.alternate;
          if (y && !B1(g)) {
            if (f = Qm(e, u), f === oc) {
              var x = af(e);
              x !== Y && (u = x, f = GS(e, x));
            }
            if (f === $p) {
              var b = Yp;
              throw cc(e, Y), Ko(e, u), Ya(e, Gn()), b;
            }
          }
          e.finishedWork = g, e.finishedLanes = u, P1(e, f, u);
        }
      }
      return Ya(e, Gn()), e.callbackNode === a ? o_.bind(null, e) : null;
    }
    function GS(e, t) {
      var a = Wp;
      if (sf(e)) {
        var i = cc(e, t);
        i.flags |= Rr, ub(e.containerInfo);
      }
      var u = Qm(e, t);
      if (u !== oc) {
        var s = Ia;
        Ia = a, s !== null && s_(s);
      }
      return u;
    }
    function s_(e) {
      Ia === null ? Ia = e : Ia.push.apply(Ia, e);
    }
    function P1(e, t, a) {
      switch (t) {
        case qu:
        case $p:
          throw new Error("Root did not complete. This is a bug in React.");
        case oc: {
          fc(e, Ia, Ku);
          break;
        }
        case jm: {
          if (Ko(e, a), Uu(a) && // do not delay if we're inside an act() scope
          !T_()) {
            var i = BS + a_ - Gn();
            if (i > 10) {
              var u = nf(e, Y);
              if (u !== Y)
                break;
              var s = e.suspendedLanes;
              if (!zu(s, a)) {
                Ra(), uf(e, s);
                break;
              }
              e.timeoutHandle = Yy(fc.bind(null, e, Ia, Ku), i);
              break;
            }
          }
          fc(e, Ia, Ku);
          break;
        }
        case Ip: {
          if (Ko(e, a), jd(a))
            break;
          if (!T_()) {
            var f = oi(e, a), p = f, v = Gn() - p, y = ux(v) - v;
            if (y > 10) {
              e.timeoutHandle = Yy(fc.bind(null, e, Ia, Ku), y);
              break;
            }
          }
          fc(e, Ia, Ku);
          break;
        }
        case r_: {
          fc(e, Ia, Ku);
          break;
        }
        default:
          throw new Error("Unknown root exit status.");
      }
    }
    function B1(e) {
      for (var t = e; ; ) {
        if (t.flags & Co) {
          var a = t.updateQueue;
          if (a !== null) {
            var i = a.stores;
            if (i !== null)
              for (var u = 0; u < i.length; u++) {
                var s = i[u], f = s.getSnapshot, p = s.value;
                try {
                  if (!G(f(), p))
                    return !1;
                } catch {
                  return !1;
                }
              }
          }
        }
        var v = t.child;
        if (t.subtreeFlags & Co && v !== null) {
          v.return = t, t = v;
          continue;
        }
        if (t === e)
          return !0;
        for (; t.sibling === null; ) {
          if (t.return === null || t.return === e)
            return !0;
          t = t.return;
        }
        t.sibling.return = t.return, t = t.sibling;
      }
      return !0;
    }
    function Ko(e, t) {
      t = Ns(t, Hm), t = Ns(t, Qp), Xv(e, t);
    }
    function c_(e) {
      if (iw(), (Rt & (Ir | Pi)) !== mr)
        throw new Error("Should not already be working.");
      Zu();
      var t = nf(e, Y);
      if (!na(t, Pe))
        return Ya(e, Gn()), null;
      var a = Qm(e, t);
      if (e.tag !== Fo && a === oc) {
        var i = af(e);
        i !== Y && (t = i, a = GS(e, i));
      }
      if (a === $p) {
        var u = Yp;
        throw cc(e, Y), Ko(e, t), Ya(e, Gn()), u;
      }
      if (a === VS)
        throw new Error("Root did not complete. This is a bug in React.");
      var s = e.current.alternate;
      return e.finishedWork = s, e.finishedLanes = t, fc(e, Ia, Ku), Ya(e, Gn()), null;
    }
    function $1(e, t) {
      t !== Y && (of(e, et(t, Pe)), Ya(e, Gn()), (Rt & (Ir | Pi)) === mr && (Gp(), Ho()));
    }
    function qS(e, t) {
      var a = Rt;
      Rt |= n_;
      try {
        return e(t);
      } finally {
        Rt = a, Rt === mr && // Treat `act` as if it's inside `batchedUpdates`, even in legacy mode.
        !ml.isBatchingLegacy && (Gp(), uC());
      }
    }
    function I1(e, t, a, i, u) {
      var s = Ha(), f = $r.transition;
      try {
        return $r.transition = null, Fn(Mr), e(t, a, i, u);
      } finally {
        Fn(s), $r.transition = f, Rt === mr && Gp();
      }
    }
    function Xu(e) {
      Go !== null && Go.tag === Fo && (Rt & (Ir | Pi)) === mr && Zu();
      var t = Rt;
      Rt |= n_;
      var a = $r.transition, i = Ha();
      try {
        return $r.transition = null, Fn(Mr), e ? e() : void 0;
      } finally {
        Fn(i), $r.transition = a, Rt = t, (Rt & (Ir | Pi)) === mr && Ho();
      }
    }
    function f_() {
      return (Rt & (Ir | Pi)) !== mr;
    }
    function Ym(e, t) {
      ua(PS, au, e), au = et(au, t);
    }
    function KS(e) {
      au = PS.current, la(PS, e);
    }
    function cc(e, t) {
      e.finishedWork = null, e.finishedLanes = Y;
      var a = e.timeoutHandle;
      if (a !== Qy && (e.timeoutHandle = Qy, yT(a)), On !== null)
        for (var i = On.return; i !== null; ) {
          var u = i.alternate;
          V0(u, i), i = i.return;
        }
      _a = e;
      var s = dc(e.current, null);
      return On = s, yr = au = t, gr = qu, Yp = null, Fm = Y, Qp = Y, Hm = Y, Wp = null, Ia = null, Hb(), ol.discardPendingWarnings(), s;
    }
    function d_(e, t) {
      do {
        var a = On;
        try {
          if (tm(), AC(), cn(), HS.current = null, a === null || a.return === null) {
            gr = $p, Yp = t, On = null;
            return;
          }
          if (Fe && a.mode & Mt && Om(a, !0), $e)
            if (ga(), t !== null && typeof t == "object" && typeof t.then == "function") {
              var i = t;
              Oi(a, i, yr);
            } else
              gs(a, t, yr);
          vw(e, a.return, a, t, yr), m_(a);
        } catch (u) {
          t = u, On === a && a !== null ? (a = a.return, On = a) : a = On;
          continue;
        }
        return;
      } while (!0);
    }
    function p_() {
      var e = FS.current;
      return FS.current = bm, e === null ? bm : e;
    }
    function v_(e) {
      FS.current = e;
    }
    function Y1() {
      BS = Gn();
    }
    function Zp(e) {
      Fm = et(e, Fm);
    }
    function Q1() {
      gr === qu && (gr = jm);
    }
    function XS() {
      (gr === qu || gr === jm || gr === oc) && (gr = Ip), _a !== null && (Ds(Fm) || Ds(Qp)) && Ko(_a, yr);
    }
    function W1(e) {
      gr !== Ip && (gr = oc), Wp === null ? Wp = [e] : Wp.push(e);
    }
    function G1() {
      return gr === qu;
    }
    function Qm(e, t) {
      var a = Rt;
      Rt |= Ir;
      var i = p_();
      if (_a !== e || yr !== t) {
        if (ea) {
          var u = e.memoizedUpdaters;
          u.size > 0 && (Jp(e, yr), u.clear()), Zv(e, t);
        }
        Ku = $d(), cc(e, t);
      }
      xu(t);
      do
        try {
          q1();
          break;
        } catch (s) {
          d_(e, s);
        }
      while (!0);
      if (tm(), Rt = a, v_(i), On !== null)
        throw new Error("Cannot commit an incomplete root. This error is likely caused by a bug in React. Please file an issue.");
      return Fc(), _a = null, yr = Y, gr;
    }
    function q1() {
      for (; On !== null; )
        h_(On);
    }
    function K1(e, t) {
      var a = Rt;
      Rt |= Ir;
      var i = p_();
      if (_a !== e || yr !== t) {
        if (ea) {
          var u = e.memoizedUpdaters;
          u.size > 0 && (Jp(e, yr), u.clear()), Zv(e, t);
        }
        Ku = $d(), Gp(), cc(e, t);
      }
      xu(t);
      do
        try {
          X1();
          break;
        } catch (s) {
          d_(e, s);
        }
      while (!0);
      return tm(), v_(i), Rt = a, On !== null ? ($v(), qu) : (Fc(), _a = null, yr = Y, gr);
    }
    function X1() {
      for (; On !== null && !_d(); )
        h_(On);
    }
    function h_(e) {
      var t = e.alternate;
      Qt(e);
      var a;
      (e.mode & Mt) !== Ne ? (eS(e), a = ZS(t, e, au), Om(e, !0)) : a = ZS(t, e, au), cn(), e.memoizedProps = e.pendingProps, a === null ? m_(e) : On = a, HS.current = null;
    }
    function m_(e) {
      var t = e;
      do {
        var a = t.alternate, i = t.return;
        if ((t.flags & hs) === Oe) {
          Qt(t);
          var u = void 0;
          if ((t.mode & Mt) === Ne ? u = H0(a, t, au) : (eS(t), u = H0(a, t, au), Om(t, !1)), cn(), u !== null) {
            On = u;
            return;
          }
        } else {
          var s = Qw(a, t);
          if (s !== null) {
            s.flags &= jv, On = s;
            return;
          }
          if ((t.mode & Mt) !== Ne) {
            Om(t, !1);
            for (var f = t.actualDuration, p = t.child; p !== null; )
              f += p.actualDuration, p = p.sibling;
            t.actualDuration = f;
          }
          if (i !== null)
            i.flags |= hs, i.subtreeFlags = Oe, i.deletions = null;
          else {
            gr = VS, On = null;
            return;
          }
        }
        var v = t.sibling;
        if (v !== null) {
          On = v;
          return;
        }
        t = i, On = t;
      } while (t !== null);
      gr === qu && (gr = r_);
    }
    function fc(e, t, a) {
      var i = Ha(), u = $r.transition;
      try {
        $r.transition = null, Fn(Mr), Z1(e, t, a, i);
      } finally {
        $r.transition = u, Fn(i);
      }
      return null;
    }
    function Z1(e, t, a, i) {
      do
        Zu();
      while (Go !== null);
      if (sx(), (Rt & (Ir | Pi)) !== mr)
        throw new Error("Should not already be working.");
      var u = e.finishedWork, s = e.finishedLanes;
      if (kd(s), u === null)
        return Dd(), null;
      if (s === Y && S("root.finishedLanes should not be empty during a commit. This is a bug in React."), e.finishedWork = null, e.finishedLanes = Y, u === e.current)
        throw new Error("Cannot commit the same tree as before. This error is likely caused by a bug in React. Please file an issue.");
      e.callbackNode = null, e.callbackPriority = Ot;
      var f = et(u.lanes, u.childLanes);
      Pd(e, f), e === _a && (_a = null, On = null, yr = Y), ((u.subtreeFlags & Zi) !== Oe || (u.flags & Zi) !== Oe) && (sc || (sc = !0, YS = a, tE(Ji, function() {
        return Zu(), null;
      })));
      var p = (u.subtreeFlags & (zl | Al | jl | Zi)) !== Oe, v = (u.flags & (zl | Al | jl | Zi)) !== Oe;
      if (p || v) {
        var y = $r.transition;
        $r.transition = null;
        var g = Ha();
        Fn(Mr);
        var x = Rt;
        Rt |= Pi, HS.current = null, Xw(e, u), u0(), f1(e, u, s), cT(e.containerInfo), e.current = u, Ss(s), d1(u, e, s), Es(), Rd(), Rt = x, Fn(g), $r.transition = y;
      } else
        e.current = u, u0();
      var b = sc;
      if (sc ? (sc = !1, Go = e, qp = s) : (qf = 0, Bm = null), f = e.pendingLanes, f === Y && (Gf = null), b || E_(e.current, !1), bd(u.stateNode, i), ea && e.memoizedUpdaters.clear(), N1(), Ya(e, Gn()), t !== null)
        for (var U = e.onRecoverableError, F = 0; F < t.length; F++) {
          var V = t[F], ce = V.stack, Ue = V.digest;
          U(V.value, {
            componentStack: ce,
            digest: Ue
          });
        }
      if (Vm) {
        Vm = !1;
        var we = $S;
        throw $S = null, we;
      }
      return na(qp, Pe) && e.tag !== Fo && Zu(), f = e.pendingLanes, na(f, Pe) ? (rw(), e === QS ? Kp++ : (Kp = 0, QS = e)) : Kp = 0, Ho(), Dd(), null;
    }
    function Zu() {
      if (Go !== null) {
        var e = th(qp), t = zs(ja, e), a = $r.transition, i = Ha();
        try {
          return $r.transition = null, Fn(t), ex();
        } finally {
          Fn(i), $r.transition = a;
        }
      }
      return !1;
    }
    function J1(e) {
      IS.push(e), sc || (sc = !0, tE(Ji, function() {
        return Zu(), null;
      }));
    }
    function ex() {
      if (Go === null)
        return !1;
      var e = YS;
      YS = null;
      var t = Go, a = qp;
      if (Go = null, qp = Y, (Rt & (Ir | Pi)) !== mr)
        throw new Error("Cannot flush passive effects while already rendering.");
      WS = !0, Pm = !1, wu(a);
      var i = Rt;
      Rt |= Pi, S1(t.current), h1(t, t.current, a, e);
      {
        var u = IS;
        IS = [];
        for (var s = 0; s < u.length; s++) {
          var f = u[s];
          t1(t, f);
        }
      }
      Ld(), E_(t.current, !0), Rt = i, Ho(), Pm ? t === Bm ? qf++ : (qf = 0, Bm = t) : qf = 0, WS = !1, Pm = !1, wd(t);
      {
        var p = t.current.stateNode;
        p.effectDuration = 0, p.passiveEffectDuration = 0;
      }
      return !0;
    }
    function y_(e) {
      return Gf !== null && Gf.has(e);
    }
    function tx(e) {
      Gf === null ? Gf = /* @__PURE__ */ new Set([e]) : Gf.add(e);
    }
    function nx(e) {
      Vm || (Vm = !0, $S = e);
    }
    var rx = nx;
    function g_(e, t, a) {
      var i = lc(a, t), u = h0(e, i, Pe), s = Po(e, u, Pe), f = Ra();
      s !== null && (wo(s, Pe, f), Ya(s, f));
    }
    function fn(e, t, a) {
      if (Gw(a), ev(!1), e.tag === te) {
        g_(e, e, a);
        return;
      }
      var i = null;
      for (i = t; i !== null; ) {
        if (i.tag === te) {
          g_(i, e, a);
          return;
        } else if (i.tag === ne) {
          var u = i.type, s = i.stateNode;
          if (typeof u.getDerivedStateFromError == "function" || typeof s.componentDidCatch == "function" && !y_(s)) {
            var f = lc(a, e), p = gS(i, f, Pe), v = Po(i, p, Pe), y = Ra();
            v !== null && (wo(v, Pe, y), Ya(v, y));
            return;
          }
        }
        i = i.return;
      }
      S(`Internal React error: Attempted to capture a commit phase error inside a detached tree. This indicates a bug in React. Likely causes include deleting the same fiber more than once, committing an already-finished tree, or an inconsistent return pointer.

Error message:

%s`, a);
    }
    function ax(e, t, a) {
      var i = e.pingCache;
      i !== null && i.delete(t);
      var u = Ra();
      uf(e, a), px(e), _a === e && zu(yr, a) && (gr === Ip || gr === jm && Uu(yr) && Gn() - BS < a_ ? cc(e, Y) : Hm = et(Hm, a)), Ya(e, u);
    }
    function S_(e, t) {
      t === Ot && (t = F1(e));
      var a = Ra(), i = Ba(e, t);
      i !== null && (wo(i, t, a), Ya(i, a));
    }
    function ix(e) {
      var t = e.memoizedState, a = Ot;
      t !== null && (a = t.retryLane), S_(e, a);
    }
    function lx(e, t) {
      var a = Ot, i;
      switch (e.tag) {
        case De:
          i = e.stateNode;
          var u = e.memoizedState;
          u !== null && (a = u.retryLane);
          break;
        case un:
          i = e.stateNode;
          break;
        default:
          throw new Error("Pinged unknown suspense boundary type. This is probably a bug in React.");
      }
      i !== null && i.delete(t), S_(e, a);
    }
    function ux(e) {
      return e < 120 ? 120 : e < 480 ? 480 : e < 1080 ? 1080 : e < 1920 ? 1920 : e < 3e3 ? 3e3 : e < 4320 ? 4320 : U1(e / 1960) * 1960;
    }
    function ox() {
      if (Kp > A1)
        throw Kp = 0, QS = null, new Error("Maximum update depth exceeded. This can happen when a component repeatedly calls setState inside componentWillUpdate or componentDidUpdate. React limits the number of nested updates to prevent infinite loops.");
      qf > j1 && (qf = 0, Bm = null, S("Maximum update depth exceeded. This can happen when a component calls setState inside useEffect, but useEffect either doesn't have a dependency array, or one of the dependencies changes on every render."));
    }
    function sx() {
      ol.flushLegacyContextWarning(), ol.flushPendingUnsafeLifecycleWarnings();
    }
    function E_(e, t) {
      Qt(e), Wm(e, Ul, k1), t && Wm(e, xi, D1), Wm(e, Ul, w1), t && Wm(e, xi, x1), cn();
    }
    function Wm(e, t, a) {
      for (var i = e, u = null; i !== null; ) {
        var s = i.subtreeFlags & t;
        i !== u && i.child !== null && s !== Oe ? i = i.child : ((i.flags & t) !== Oe && a(i), i.sibling !== null ? i = i.sibling : i = u = i.return);
      }
    }
    var Gm = null;
    function C_(e) {
      {
        if ((Rt & Ir) !== mr || !(e.mode & ct))
          return;
        var t = e.tag;
        if (t !== Ve && t !== te && t !== ne && t !== ee && t !== Ke && t !== dt && t !== Be)
          return;
        var a = Qe(e) || "ReactComponent";
        if (Gm !== null) {
          if (Gm.has(a))
            return;
          Gm.add(a);
        } else
          Gm = /* @__PURE__ */ new Set([a]);
        var i = ur;
        try {
          Qt(e), S("Can't perform a React state update on a component that hasn't mounted yet. This indicates that you have a side-effect in your render function that asynchronously later calls tries to update the component. Move this work to useEffect instead.");
        } finally {
          i ? Qt(e) : cn();
        }
      }
    }
    var ZS;
    {
      var cx = null;
      ZS = function(e, t, a) {
        var i = D_(cx, t);
        try {
          return U0(e, t, a);
        } catch (s) {
          if (_b() || s !== null && typeof s == "object" && typeof s.then == "function")
            throw s;
          if (tm(), AC(), V0(e, t), D_(t, i), t.mode & Mt && eS(t), Ml(null, U0, null, e, t, a), Ki()) {
            var u = vs();
            typeof u == "object" && u !== null && u._suppressLogging && typeof s == "object" && s !== null && !s._suppressLogging && (s._suppressLogging = !0);
          }
          throw s;
        }
      };
    }
    var __ = !1, JS;
    JS = /* @__PURE__ */ new Set();
    function fx(e) {
      if (Ei && !ew())
        switch (e.tag) {
          case ee:
          case Ke:
          case Be: {
            var t = On && Qe(On) || "Unknown", a = t;
            if (!JS.has(a)) {
              JS.add(a);
              var i = Qe(e) || "Unknown";
              S("Cannot update a component (`%s`) while rendering a different component (`%s`). To locate the bad setState() call inside `%s`, follow the stack trace as described in https://reactjs.org/link/setstate-in-render", i, t, t);
            }
            break;
          }
          case ne: {
            __ || (S("Cannot update during an existing state transition (such as within `render`). Render methods should be a pure function of props and state."), __ = !0);
            break;
          }
        }
    }
    function Jp(e, t) {
      if (ea) {
        var a = e.memoizedUpdaters;
        a.forEach(function(i) {
          Ms(e, i, t);
        });
      }
    }
    var eE = {};
    function tE(e, t) {
      {
        var a = ml.current;
        return a !== null ? (a.push(t), eE) : Cd(e, t);
      }
    }
    function R_(e) {
      if (e !== eE)
        return Hv(e);
    }
    function T_() {
      return ml.current !== null;
    }
    function dx(e) {
      {
        if (e.mode & ct) {
          if (!t_())
            return;
        } else if (!M1() || Rt !== mr || e.tag !== ee && e.tag !== Ke && e.tag !== Be)
          return;
        if (ml.current === null) {
          var t = ur;
          try {
            Qt(e), S(`An update to %s inside a test was not wrapped in act(...).

When testing, code that causes React state updates should be wrapped into act(...):

act(() => {
  /* fire events that update state */
});
/* assert on the output */

This ensures that you're testing the behavior the user would see in the browser. Learn more at https://reactjs.org/link/wrap-tests-with-act`, Qe(e));
          } finally {
            t ? Qt(e) : cn();
          }
        }
      }
    }
    function px(e) {
      e.tag !== Fo && t_() && ml.current === null && S(`A suspended resource finished loading inside a test, but the event was not wrapped in act(...).

When testing, code that resolves suspended data should be wrapped into act(...):

act(() => {
  /* finish loading suspended data */
});
/* assert on the output */

This ensures that you're testing the behavior the user would see in the browser. Learn more at https://reactjs.org/link/wrap-tests-with-act`);
    }
    function ev(e) {
      u_ = e;
    }
    var Bi = null, Kf = null, vx = function(e) {
      Bi = e;
    };
    function Xf(e) {
      {
        if (Bi === null)
          return e;
        var t = Bi(e);
        return t === void 0 ? e : t.current;
      }
    }
    function nE(e) {
      return Xf(e);
    }
    function rE(e) {
      {
        if (Bi === null)
          return e;
        var t = Bi(e);
        if (t === void 0) {
          if (e != null && typeof e.render == "function") {
            var a = Xf(e.render);
            if (e.render !== a) {
              var i = {
                $$typeof: I,
                render: a
              };
              return e.displayName !== void 0 && (i.displayName = e.displayName), i;
            }
          }
          return e;
        }
        return t.current;
      }
    }
    function b_(e, t) {
      {
        if (Bi === null)
          return !1;
        var a = e.elementType, i = t.type, u = !1, s = typeof i == "object" && i !== null ? i.$$typeof : null;
        switch (e.tag) {
          case ne: {
            typeof i == "function" && (u = !0);
            break;
          }
          case ee: {
            (typeof i == "function" || s === We) && (u = !0);
            break;
          }
          case Ke: {
            (s === I || s === We) && (u = !0);
            break;
          }
          case dt:
          case Be: {
            (s === Ze || s === We) && (u = !0);
            break;
          }
          default:
            return !1;
        }
        if (u) {
          var f = Bi(a);
          if (f !== void 0 && f === Bi(i))
            return !0;
        }
        return !1;
      }
    }
    function w_(e) {
      {
        if (Bi === null || typeof WeakSet != "function")
          return;
        Kf === null && (Kf = /* @__PURE__ */ new WeakSet()), Kf.add(e);
      }
    }
    var hx = function(e, t) {
      {
        if (Bi === null)
          return;
        var a = t.staleFamilies, i = t.updatedFamilies;
        Zu(), Xu(function() {
          aE(e.current, i, a);
        });
      }
    }, mx = function(e, t) {
      {
        if (e.context !== fi)
          return;
        Zu(), Xu(function() {
          tv(t, e, null, null);
        });
      }
    };
    function aE(e, t, a) {
      {
        var i = e.alternate, u = e.child, s = e.sibling, f = e.tag, p = e.type, v = null;
        switch (f) {
          case ee:
          case Be:
          case ne:
            v = p;
            break;
          case Ke:
            v = p.render;
            break;
        }
        if (Bi === null)
          throw new Error("Expected resolveFamily to be set during hot reload.");
        var y = !1, g = !1;
        if (v !== null) {
          var x = Bi(v);
          x !== void 0 && (a.has(x) ? g = !0 : t.has(x) && (f === ne ? g = !0 : y = !0));
        }
        if (Kf !== null && (Kf.has(e) || i !== null && Kf.has(i)) && (g = !0), g && (e._debugNeedsRemount = !0), g || y) {
          var b = Ba(e, Pe);
          b !== null && Sr(b, e, Pe, Zt);
        }
        u !== null && !g && aE(u, t, a), s !== null && aE(s, t, a);
      }
    }
    var yx = function(e, t) {
      {
        var a = /* @__PURE__ */ new Set(), i = new Set(t.map(function(u) {
          return u.current;
        }));
        return iE(e.current, i, a), a;
      }
    };
    function iE(e, t, a) {
      {
        var i = e.child, u = e.sibling, s = e.tag, f = e.type, p = null;
        switch (s) {
          case ee:
          case Be:
          case ne:
            p = f;
            break;
          case Ke:
            p = f.render;
            break;
        }
        var v = !1;
        p !== null && t.has(p) && (v = !0), v ? gx(e, a) : i !== null && iE(i, t, a), u !== null && iE(u, t, a);
      }
    }
    function gx(e, t) {
      {
        var a = Sx(e, t);
        if (a)
          return;
        for (var i = e; ; ) {
          switch (i.tag) {
            case fe:
              t.add(i.stateNode);
              return;
            case me:
              t.add(i.stateNode.containerInfo);
              return;
            case te:
              t.add(i.stateNode.containerInfo);
              return;
          }
          if (i.return === null)
            throw new Error("Expected to reach root first.");
          i = i.return;
        }
      }
    }
    function Sx(e, t) {
      for (var a = e, i = !1; ; ) {
        if (a.tag === fe)
          i = !0, t.add(a.stateNode);
        else if (a.child !== null) {
          a.child.return = a, a = a.child;
          continue;
        }
        if (a === e)
          return i;
        for (; a.sibling === null; ) {
          if (a.return === null || a.return === e)
            return i;
          a = a.return;
        }
        a.sibling.return = a.return, a = a.sibling;
      }
      return !1;
    }
    var lE;
    {
      lE = !1;
      try {
        var x_ = Object.preventExtensions({});
      } catch {
        lE = !0;
      }
    }
    function Ex(e, t, a, i) {
      this.tag = e, this.key = a, this.elementType = null, this.type = null, this.stateNode = null, this.return = null, this.child = null, this.sibling = null, this.index = 0, this.ref = null, this.pendingProps = t, this.memoizedProps = null, this.updateQueue = null, this.memoizedState = null, this.dependencies = null, this.mode = i, this.flags = Oe, this.subtreeFlags = Oe, this.deletions = null, this.lanes = Y, this.childLanes = Y, this.alternate = null, this.actualDuration = Number.NaN, this.actualStartTime = Number.NaN, this.selfBaseDuration = Number.NaN, this.treeBaseDuration = Number.NaN, this.actualDuration = 0, this.actualStartTime = -1, this.selfBaseDuration = 0, this.treeBaseDuration = 0, this._debugSource = null, this._debugOwner = null, this._debugNeedsRemount = !1, this._debugHookTypes = null, !lE && typeof Object.preventExtensions == "function" && Object.preventExtensions(this);
    }
    var di = function(e, t, a, i) {
      return new Ex(e, t, a, i);
    };
    function uE(e) {
      var t = e.prototype;
      return !!(t && t.isReactComponent);
    }
    function Cx(e) {
      return typeof e == "function" && !uE(e) && e.defaultProps === void 0;
    }
    function _x(e) {
      if (typeof e == "function")
        return uE(e) ? ne : ee;
      if (e != null) {
        var t = e.$$typeof;
        if (t === I)
          return Ke;
        if (t === Ze)
          return dt;
      }
      return Ve;
    }
    function dc(e, t) {
      var a = e.alternate;
      a === null ? (a = di(e.tag, t, e.key, e.mode), a.elementType = e.elementType, a.type = e.type, a.stateNode = e.stateNode, a._debugSource = e._debugSource, a._debugOwner = e._debugOwner, a._debugHookTypes = e._debugHookTypes, a.alternate = e, e.alternate = a) : (a.pendingProps = t, a.type = e.type, a.flags = Oe, a.subtreeFlags = Oe, a.deletions = null, a.actualDuration = 0, a.actualStartTime = -1), a.flags = e.flags & zn, a.childLanes = e.childLanes, a.lanes = e.lanes, a.child = e.child, a.memoizedProps = e.memoizedProps, a.memoizedState = e.memoizedState, a.updateQueue = e.updateQueue;
      var i = e.dependencies;
      switch (a.dependencies = i === null ? null : {
        lanes: i.lanes,
        firstContext: i.firstContext
      }, a.sibling = e.sibling, a.index = e.index, a.ref = e.ref, a.selfBaseDuration = e.selfBaseDuration, a.treeBaseDuration = e.treeBaseDuration, a._debugNeedsRemount = e._debugNeedsRemount, a.tag) {
        case Ve:
        case ee:
        case Be:
          a.type = Xf(e.type);
          break;
        case ne:
          a.type = nE(e.type);
          break;
        case Ke:
          a.type = rE(e.type);
          break;
      }
      return a;
    }
    function Rx(e, t) {
      e.flags &= zn | yn;
      var a = e.alternate;
      if (a === null)
        e.childLanes = Y, e.lanes = t, e.child = null, e.subtreeFlags = Oe, e.memoizedProps = null, e.memoizedState = null, e.updateQueue = null, e.dependencies = null, e.stateNode = null, e.selfBaseDuration = 0, e.treeBaseDuration = 0;
      else {
        e.childLanes = a.childLanes, e.lanes = a.lanes, e.child = a.child, e.subtreeFlags = Oe, e.deletions = null, e.memoizedProps = a.memoizedProps, e.memoizedState = a.memoizedState, e.updateQueue = a.updateQueue, e.type = a.type;
        var i = a.dependencies;
        e.dependencies = i === null ? null : {
          lanes: i.lanes,
          firstContext: i.firstContext
        }, e.selfBaseDuration = a.selfBaseDuration, e.treeBaseDuration = a.treeBaseDuration;
      }
      return e;
    }
    function Tx(e, t, a) {
      var i;
      return e === Yh ? (i = ct, t === !0 && (i |= qt, i |= Ut)) : i = Ne, ea && (i |= Mt), di(te, null, null, i);
    }
    function oE(e, t, a, i, u, s) {
      var f = Ve, p = e;
      if (typeof e == "function")
        uE(e) ? (f = ne, p = nE(p)) : p = Xf(p);
      else if (typeof e == "string")
        f = fe;
      else
        e: switch (e) {
          case mi:
            return Xo(a.children, u, s, t);
          case Xa:
            f = mt, u |= qt, (u & ct) !== Ne && (u |= Ut);
            break;
          case yi:
            return bx(a, u, s, t);
          case ue:
            return wx(a, u, s, t);
          case ge:
            return xx(a, u, s, t);
          case Tn:
            return k_(a, u, s, t);
          case nn:
          case pt:
          case sn:
          case lr:
          case st:
          default: {
            if (typeof e == "object" && e !== null)
              switch (e.$$typeof) {
                case gi:
                  f = ht;
                  break e;
                case _:
                  f = dn;
                  break e;
                case I:
                  f = Ke, p = rE(p);
                  break e;
                case Ze:
                  f = dt;
                  break e;
                case We:
                  f = ln, p = null;
                  break e;
              }
            var v = "";
            {
              (e === void 0 || typeof e == "object" && e !== null && Object.keys(e).length === 0) && (v += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
              var y = i ? Qe(i) : null;
              y && (v += `

Check the render method of \`` + y + "`.");
            }
            throw new Error("Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) " + ("but got: " + (e == null ? e : typeof e) + "." + v));
          }
        }
      var g = di(f, a, t, u);
      return g.elementType = e, g.type = p, g.lanes = s, g._debugOwner = i, g;
    }
    function sE(e, t, a) {
      var i = null;
      i = e._owner;
      var u = e.type, s = e.key, f = e.props, p = oE(u, s, f, i, t, a);
      return p._debugSource = e._source, p._debugOwner = e._owner, p;
    }
    function Xo(e, t, a, i) {
      var u = di(Et, e, i, t);
      return u.lanes = a, u;
    }
    function bx(e, t, a, i) {
      typeof e.id != "string" && S('Profiler must specify an "id" of type `string` as a prop. Received the type `%s` instead.', typeof e.id);
      var u = di(yt, e, i, t | Mt);
      return u.elementType = yi, u.lanes = a, u.stateNode = {
        effectDuration: 0,
        passiveEffectDuration: 0
      }, u;
    }
    function wx(e, t, a, i) {
      var u = di(De, e, i, t);
      return u.elementType = ue, u.lanes = a, u;
    }
    function xx(e, t, a, i) {
      var u = di(un, e, i, t);
      return u.elementType = ge, u.lanes = a, u;
    }
    function k_(e, t, a, i) {
      var u = di(Le, e, i, t);
      u.elementType = Tn, u.lanes = a;
      var s = {
        isHidden: !1
      };
      return u.stateNode = s, u;
    }
    function cE(e, t, a) {
      var i = di(qe, e, null, t);
      return i.lanes = a, i;
    }
    function kx() {
      var e = di(fe, null, null, Ne);
      return e.elementType = "DELETED", e;
    }
    function Dx(e) {
      var t = di(Jt, null, null, Ne);
      return t.stateNode = e, t;
    }
    function fE(e, t, a) {
      var i = e.children !== null ? e.children : [], u = di(me, i, e.key, t);
      return u.lanes = a, u.stateNode = {
        containerInfo: e.containerInfo,
        pendingChildren: null,
        // Used by persistent updates
        implementation: e.implementation
      }, u;
    }
    function D_(e, t) {
      return e === null && (e = di(Ve, null, null, Ne)), e.tag = t.tag, e.key = t.key, e.elementType = t.elementType, e.type = t.type, e.stateNode = t.stateNode, e.return = t.return, e.child = t.child, e.sibling = t.sibling, e.index = t.index, e.ref = t.ref, e.pendingProps = t.pendingProps, e.memoizedProps = t.memoizedProps, e.updateQueue = t.updateQueue, e.memoizedState = t.memoizedState, e.dependencies = t.dependencies, e.mode = t.mode, e.flags = t.flags, e.subtreeFlags = t.subtreeFlags, e.deletions = t.deletions, e.lanes = t.lanes, e.childLanes = t.childLanes, e.alternate = t.alternate, e.actualDuration = t.actualDuration, e.actualStartTime = t.actualStartTime, e.selfBaseDuration = t.selfBaseDuration, e.treeBaseDuration = t.treeBaseDuration, e._debugSource = t._debugSource, e._debugOwner = t._debugOwner, e._debugNeedsRemount = t._debugNeedsRemount, e._debugHookTypes = t._debugHookTypes, e;
    }
    function Ox(e, t, a, i, u) {
      this.tag = t, this.containerInfo = e, this.pendingChildren = null, this.current = null, this.pingCache = null, this.finishedWork = null, this.timeoutHandle = Qy, this.context = null, this.pendingContext = null, this.callbackNode = null, this.callbackPriority = Ot, this.eventTimes = Ls(Y), this.expirationTimes = Ls(Zt), this.pendingLanes = Y, this.suspendedLanes = Y, this.pingedLanes = Y, this.expiredLanes = Y, this.mutableReadLanes = Y, this.finishedLanes = Y, this.entangledLanes = Y, this.entanglements = Ls(Y), this.identifierPrefix = i, this.onRecoverableError = u, this.mutableSourceEagerHydrationData = null, this.effectDuration = 0, this.passiveEffectDuration = 0;
      {
        this.memoizedUpdaters = /* @__PURE__ */ new Set();
        for (var s = this.pendingUpdatersLaneMap = [], f = 0; f < ku; f++)
          s.push(/* @__PURE__ */ new Set());
      }
      switch (t) {
        case Yh:
          this._debugRootType = a ? "hydrateRoot()" : "createRoot()";
          break;
        case Fo:
          this._debugRootType = a ? "hydrate()" : "render()";
          break;
      }
    }
    function O_(e, t, a, i, u, s, f, p, v, y) {
      var g = new Ox(e, t, a, p, v), x = Tx(t, s);
      g.current = x, x.stateNode = g;
      {
        var b = {
          element: i,
          isDehydrated: a,
          cache: null,
          // not enabled yet
          transitions: null,
          pendingSuspenseBoundaries: null
        };
        x.memoizedState = b;
      }
      return Tg(x), g;
    }
    var dE = "18.3.1";
    function Nx(e, t, a) {
      var i = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : null;
      return Wr(i), {
        // This tag allow us to uniquely identify this as a React Portal
        $$typeof: ir,
        key: i == null ? null : "" + i,
        children: e,
        containerInfo: t,
        implementation: a
      };
    }
    var pE, vE;
    pE = !1, vE = {};
    function N_(e) {
      if (!e)
        return fi;
      var t = Eo(e), a = pb(t);
      if (t.tag === ne) {
        var i = t.type;
        if (Xl(i))
          return aC(t, i, a);
      }
      return a;
    }
    function Lx(e, t) {
      {
        var a = Eo(e);
        if (a === void 0) {
          if (typeof e.render == "function")
            throw new Error("Unable to find node on an unmounted component.");
          var i = Object.keys(e).join(",");
          throw new Error("Argument appears to not be a ReactComponent. Keys: " + i);
        }
        var u = Zr(a);
        if (u === null)
          return null;
        if (u.mode & qt) {
          var s = Qe(a) || "Component";
          if (!vE[s]) {
            vE[s] = !0;
            var f = ur;
            try {
              Qt(u), a.mode & qt ? S("%s is deprecated in StrictMode. %s was passed an instance of %s which is inside StrictMode. Instead, add a ref directly to the element you want to reference. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-find-node", t, t, s) : S("%s is deprecated in StrictMode. %s was passed an instance of %s which renders StrictMode children. Instead, add a ref directly to the element you want to reference. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-find-node", t, t, s);
            } finally {
              f ? Qt(f) : cn();
            }
          }
        }
        return u.stateNode;
      }
    }
    function L_(e, t, a, i, u, s, f, p) {
      var v = !1, y = null;
      return O_(e, t, v, y, a, i, u, s, f);
    }
    function M_(e, t, a, i, u, s, f, p, v, y) {
      var g = !0, x = O_(a, i, g, e, u, s, f, p, v);
      x.context = N_(null);
      var b = x.current, U = Ra(), F = qo(b), V = Wu(U, F);
      return V.callback = t ?? null, Po(b, V, F), H1(x, F, U), x;
    }
    function tv(e, t, a, i) {
      Td(t, e);
      var u = t.current, s = Ra(), f = qo(u);
      Sn(f);
      var p = N_(a);
      t.context === null ? t.context = p : t.pendingContext = p, Ei && ur !== null && !pE && (pE = !0, S(`Render methods should be a pure function of props and state; triggering nested component updates from render is not allowed. If necessary, trigger nested updates in componentDidUpdate.

Check the render method of %s.`, Qe(ur) || "Unknown"));
      var v = Wu(s, f);
      v.payload = {
        element: e
      }, i = i === void 0 ? null : i, i !== null && (typeof i != "function" && S("render(...): Expected the last optional `callback` argument to be a function. Instead received: %s.", i), v.callback = i);
      var y = Po(u, v, f);
      return y !== null && (Sr(y, u, f, s), lm(y, u, f)), f;
    }
    function qm(e) {
      var t = e.current;
      if (!t.child)
        return null;
      switch (t.child.tag) {
        case fe:
          return t.child.stateNode;
        default:
          return t.child.stateNode;
      }
    }
    function Mx(e) {
      switch (e.tag) {
        case te: {
          var t = e.stateNode;
          if (sf(t)) {
            var a = Yv(t);
            $1(t, a);
          }
          break;
        }
        case De: {
          Xu(function() {
            var u = Ba(e, Pe);
            if (u !== null) {
              var s = Ra();
              Sr(u, e, Pe, s);
            }
          });
          var i = Pe;
          hE(e, i);
          break;
        }
      }
    }
    function U_(e, t) {
      var a = e.memoizedState;
      a !== null && a.dehydrated !== null && (a.retryLane = Kv(a.retryLane, t));
    }
    function hE(e, t) {
      U_(e, t);
      var a = e.alternate;
      a && U_(a, t);
    }
    function Ux(e) {
      if (e.tag === De) {
        var t = ws, a = Ba(e, t);
        if (a !== null) {
          var i = Ra();
          Sr(a, e, t, i);
        }
        hE(e, t);
      }
    }
    function zx(e) {
      if (e.tag === De) {
        var t = qo(e), a = Ba(e, t);
        if (a !== null) {
          var i = Ra();
          Sr(a, e, t, i);
        }
        hE(e, t);
      }
    }
    function z_(e) {
      var t = pn(e);
      return t === null ? null : t.stateNode;
    }
    var A_ = function(e) {
      return null;
    };
    function Ax(e) {
      return A_(e);
    }
    var j_ = function(e) {
      return !1;
    };
    function jx(e) {
      return j_(e);
    }
    var F_ = null, H_ = null, V_ = null, P_ = null, B_ = null, $_ = null, I_ = null, Y_ = null, Q_ = null;
    {
      var W_ = function(e, t, a) {
        var i = t[a], u = lt(e) ? e.slice() : nt({}, e);
        return a + 1 === t.length ? (lt(u) ? u.splice(i, 1) : delete u[i], u) : (u[i] = W_(e[i], t, a + 1), u);
      }, G_ = function(e, t) {
        return W_(e, t, 0);
      }, q_ = function(e, t, a, i) {
        var u = t[i], s = lt(e) ? e.slice() : nt({}, e);
        if (i + 1 === t.length) {
          var f = a[i];
          s[f] = s[u], lt(s) ? s.splice(u, 1) : delete s[u];
        } else
          s[u] = q_(
            // $FlowFixMe number or string is fine here
            e[u],
            t,
            a,
            i + 1
          );
        return s;
      }, K_ = function(e, t, a) {
        if (t.length !== a.length) {
          He("copyWithRename() expects paths of the same length");
          return;
        } else
          for (var i = 0; i < a.length - 1; i++)
            if (t[i] !== a[i]) {
              He("copyWithRename() expects paths to be the same except for the deepest key");
              return;
            }
        return q_(e, t, a, 0);
      }, X_ = function(e, t, a, i) {
        if (a >= t.length)
          return i;
        var u = t[a], s = lt(e) ? e.slice() : nt({}, e);
        return s[u] = X_(e[u], t, a + 1, i), s;
      }, Z_ = function(e, t, a) {
        return X_(e, t, 0, a);
      }, mE = function(e, t) {
        for (var a = e.memoizedState; a !== null && t > 0; )
          a = a.next, t--;
        return a;
      };
      F_ = function(e, t, a, i) {
        var u = mE(e, t);
        if (u !== null) {
          var s = Z_(u.memoizedState, a, i);
          u.memoizedState = s, u.baseState = s, e.memoizedProps = nt({}, e.memoizedProps);
          var f = Ba(e, Pe);
          f !== null && Sr(f, e, Pe, Zt);
        }
      }, H_ = function(e, t, a) {
        var i = mE(e, t);
        if (i !== null) {
          var u = G_(i.memoizedState, a);
          i.memoizedState = u, i.baseState = u, e.memoizedProps = nt({}, e.memoizedProps);
          var s = Ba(e, Pe);
          s !== null && Sr(s, e, Pe, Zt);
        }
      }, V_ = function(e, t, a, i) {
        var u = mE(e, t);
        if (u !== null) {
          var s = K_(u.memoizedState, a, i);
          u.memoizedState = s, u.baseState = s, e.memoizedProps = nt({}, e.memoizedProps);
          var f = Ba(e, Pe);
          f !== null && Sr(f, e, Pe, Zt);
        }
      }, P_ = function(e, t, a) {
        e.pendingProps = Z_(e.memoizedProps, t, a), e.alternate && (e.alternate.pendingProps = e.pendingProps);
        var i = Ba(e, Pe);
        i !== null && Sr(i, e, Pe, Zt);
      }, B_ = function(e, t) {
        e.pendingProps = G_(e.memoizedProps, t), e.alternate && (e.alternate.pendingProps = e.pendingProps);
        var a = Ba(e, Pe);
        a !== null && Sr(a, e, Pe, Zt);
      }, $_ = function(e, t, a) {
        e.pendingProps = K_(e.memoizedProps, t, a), e.alternate && (e.alternate.pendingProps = e.pendingProps);
        var i = Ba(e, Pe);
        i !== null && Sr(i, e, Pe, Zt);
      }, I_ = function(e) {
        var t = Ba(e, Pe);
        t !== null && Sr(t, e, Pe, Zt);
      }, Y_ = function(e) {
        A_ = e;
      }, Q_ = function(e) {
        j_ = e;
      };
    }
    function Fx(e) {
      var t = Zr(e);
      return t === null ? null : t.stateNode;
    }
    function Hx(e) {
      return null;
    }
    function Vx() {
      return ur;
    }
    function Px(e) {
      var t = e.findFiberByHostInstance, a = T.ReactCurrentDispatcher;
      return Ro({
        bundleType: e.bundleType,
        version: e.version,
        rendererPackageName: e.rendererPackageName,
        rendererConfig: e.rendererConfig,
        overrideHookState: F_,
        overrideHookStateDeletePath: H_,
        overrideHookStateRenamePath: V_,
        overrideProps: P_,
        overridePropsDeletePath: B_,
        overridePropsRenamePath: $_,
        setErrorHandler: Y_,
        setSuspenseHandler: Q_,
        scheduleUpdate: I_,
        currentDispatcherRef: a,
        findHostInstanceByFiber: Fx,
        findFiberByHostInstance: t || Hx,
        // React Refresh
        findHostInstancesForRefresh: yx,
        scheduleRefresh: hx,
        scheduleRoot: mx,
        setRefreshHandler: vx,
        // Enables DevTools to append owner stacks to error messages in DEV mode.
        getCurrentFiber: Vx,
        // Enables DevTools to detect reconciler version rather than renderer version
        // which may not match for third party renderers.
        reconcilerVersion: dE
      });
    }
    var J_ = typeof reportError == "function" ? (
      // In modern browsers, reportError will dispatch an error event,
      // emulating an uncaught JavaScript error.
      reportError
    ) : function(e) {
      console.error(e);
    };
    function yE(e) {
      this._internalRoot = e;
    }
    Km.prototype.render = yE.prototype.render = function(e) {
      var t = this._internalRoot;
      if (t === null)
        throw new Error("Cannot update an unmounted root.");
      {
        typeof arguments[1] == "function" ? S("render(...): does not support the second callback argument. To execute a side effect after rendering, declare it in a component body with useEffect().") : Xm(arguments[1]) ? S("You passed a container to the second argument of root.render(...). You don't need to pass it again since you already passed it to create the root.") : typeof arguments[1] < "u" && S("You passed a second argument to root.render(...) but it only accepts one argument.");
        var a = t.containerInfo;
        if (a.nodeType !== Mn) {
          var i = z_(t.current);
          i && i.parentNode !== a && S("render(...): It looks like the React-rendered content of the root container was removed without using React. This is not supported and will cause errors. Instead, call root.unmount() to empty a root's container.");
        }
      }
      tv(e, t, null, null);
    }, Km.prototype.unmount = yE.prototype.unmount = function() {
      typeof arguments[0] == "function" && S("unmount(...): does not support a callback argument. To execute a side effect after rendering, declare it in a component body with useEffect().");
      var e = this._internalRoot;
      if (e !== null) {
        this._internalRoot = null;
        var t = e.containerInfo;
        f_() && S("Attempted to synchronously unmount a root while React was already rendering. React cannot finish unmounting the root until the current render has completed, which may lead to a race condition."), Xu(function() {
          tv(null, e, null, null);
        }), JE(t);
      }
    };
    function Bx(e, t) {
      if (!Xm(e))
        throw new Error("createRoot(...): Target container is not a DOM element.");
      eR(e);
      var a = !1, i = !1, u = "", s = J_;
      t != null && (t.hydrate ? He("hydrate through createRoot is deprecated. Use ReactDOMClient.hydrateRoot(container, <App />) instead.") : typeof t == "object" && t !== null && t.$$typeof === Dr && S(`You passed a JSX element to createRoot. You probably meant to call root.render instead. Example usage:

  let root = createRoot(domContainer);
  root.render(<App />);`), t.unstable_strictMode === !0 && (a = !0), t.identifierPrefix !== void 0 && (u = t.identifierPrefix), t.onRecoverableError !== void 0 && (s = t.onRecoverableError), t.transitionCallbacks !== void 0 && t.transitionCallbacks);
      var f = L_(e, Yh, null, a, i, u, s);
      Fh(f.current, e);
      var p = e.nodeType === Mn ? e.parentNode : e;
      return up(p), new yE(f);
    }
    function Km(e) {
      this._internalRoot = e;
    }
    function $x(e) {
      e && lh(e);
    }
    Km.prototype.unstable_scheduleHydration = $x;
    function Ix(e, t, a) {
      if (!Xm(e))
        throw new Error("hydrateRoot(...): Target container is not a DOM element.");
      eR(e), t === void 0 && S("Must provide initial children as second argument to hydrateRoot. Example usage: hydrateRoot(domContainer, <App />)");
      var i = a ?? null, u = a != null && a.hydratedSources || null, s = !1, f = !1, p = "", v = J_;
      a != null && (a.unstable_strictMode === !0 && (s = !0), a.identifierPrefix !== void 0 && (p = a.identifierPrefix), a.onRecoverableError !== void 0 && (v = a.onRecoverableError));
      var y = M_(t, null, e, Yh, i, s, f, p, v);
      if (Fh(y.current, e), up(e), u)
        for (var g = 0; g < u.length; g++) {
          var x = u[g];
          Gb(y, x);
        }
      return new Km(y);
    }
    function Xm(e) {
      return !!(e && (e.nodeType === qr || e.nodeType === qi || e.nodeType === sd));
    }
    function nv(e) {
      return !!(e && (e.nodeType === qr || e.nodeType === qi || e.nodeType === sd || e.nodeType === Mn && e.nodeValue === " react-mount-point-unstable "));
    }
    function eR(e) {
      e.nodeType === qr && e.tagName && e.tagName.toUpperCase() === "BODY" && S("createRoot(): Creating roots directly with document.body is discouraged, since its children are often manipulated by third-party scripts and browser extensions. This may lead to subtle reconciliation issues. Try using a container element created for your app."), gp(e) && (e._reactRootContainer ? S("You are calling ReactDOMClient.createRoot() on a container that was previously passed to ReactDOM.render(). This is not supported.") : S("You are calling ReactDOMClient.createRoot() on a container that has already been passed to createRoot() before. Instead, call root.render() on the existing root instead if you want to update it."));
    }
    var Yx = T.ReactCurrentOwner, tR;
    tR = function(e) {
      if (e._reactRootContainer && e.nodeType !== Mn) {
        var t = z_(e._reactRootContainer.current);
        t && t.parentNode !== e && S("render(...): It looks like the React-rendered content of this container was removed without using React. This is not supported and will cause errors. Instead, call ReactDOM.unmountComponentAtNode to empty a container.");
      }
      var a = !!e._reactRootContainer, i = gE(e), u = !!(i && Ao(i));
      u && !a && S("render(...): Replacing React-rendered children with a new root component. If you intended to update the children of this node, you should instead have the existing children update their state and render the new components instead of calling ReactDOM.render."), e.nodeType === qr && e.tagName && e.tagName.toUpperCase() === "BODY" && S("render(): Rendering components directly into document.body is discouraged, since its children are often manipulated by third-party scripts and browser extensions. This may lead to subtle reconciliation issues. Try rendering into a container element created for your app.");
    };
    function gE(e) {
      return e ? e.nodeType === qi ? e.documentElement : e.firstChild : null;
    }
    function nR() {
    }
    function Qx(e, t, a, i, u) {
      if (u) {
        if (typeof i == "function") {
          var s = i;
          i = function() {
            var b = qm(f);
            s.call(b);
          };
        }
        var f = M_(
          t,
          i,
          e,
          Fo,
          null,
          // hydrationCallbacks
          !1,
          // isStrictMode
          !1,
          // concurrentUpdatesByDefaultOverride,
          "",
          // identifierPrefix
          nR
        );
        e._reactRootContainer = f, Fh(f.current, e);
        var p = e.nodeType === Mn ? e.parentNode : e;
        return up(p), Xu(), f;
      } else {
        for (var v; v = e.lastChild; )
          e.removeChild(v);
        if (typeof i == "function") {
          var y = i;
          i = function() {
            var b = qm(g);
            y.call(b);
          };
        }
        var g = L_(
          e,
          Fo,
          null,
          // hydrationCallbacks
          !1,
          // isStrictMode
          !1,
          // concurrentUpdatesByDefaultOverride,
          "",
          // identifierPrefix
          nR
        );
        e._reactRootContainer = g, Fh(g.current, e);
        var x = e.nodeType === Mn ? e.parentNode : e;
        return up(x), Xu(function() {
          tv(t, g, a, i);
        }), g;
      }
    }
    function Wx(e, t) {
      e !== null && typeof e != "function" && S("%s(...): Expected the last optional `callback` argument to be a function. Instead received: %s.", t, e);
    }
    function Zm(e, t, a, i, u) {
      tR(a), Wx(u === void 0 ? null : u, "render");
      var s = a._reactRootContainer, f;
      if (!s)
        f = Qx(a, t, e, u, i);
      else {
        if (f = s, typeof u == "function") {
          var p = u;
          u = function() {
            var v = qm(f);
            p.call(v);
          };
        }
        tv(t, f, e, u);
      }
      return qm(f);
    }
    var rR = !1;
    function Gx(e) {
      {
        rR || (rR = !0, S("findDOMNode is deprecated and will be removed in the next major release. Instead, add a ref directly to the element you want to reference. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-find-node"));
        var t = Yx.current;
        if (t !== null && t.stateNode !== null) {
          var a = t.stateNode._warnedAboutRefsInRender;
          a || S("%s is accessing findDOMNode inside its render(). render() should be a pure function of props and state. It should never access something that requires stale data from the previous render, such as refs. Move this logic to componentDidMount and componentDidUpdate instead.", wt(t.type) || "A component"), t.stateNode._warnedAboutRefsInRender = !0;
        }
      }
      return e == null ? null : e.nodeType === qr ? e : Lx(e, "findDOMNode");
    }
    function qx(e, t, a) {
      if (S("ReactDOM.hydrate is no longer supported in React 18. Use hydrateRoot instead. Until you switch to the new API, your app will behave as if it's running React 17. Learn more: https://reactjs.org/link/switch-to-createroot"), !nv(t))
        throw new Error("Target container is not a DOM element.");
      {
        var i = gp(t) && t._reactRootContainer === void 0;
        i && S("You are calling ReactDOM.hydrate() on a container that was previously passed to ReactDOMClient.createRoot(). This is not supported. Did you mean to call hydrateRoot(container, element)?");
      }
      return Zm(null, e, t, !0, a);
    }
    function Kx(e, t, a) {
      if (S("ReactDOM.render is no longer supported in React 18. Use createRoot instead. Until you switch to the new API, your app will behave as if it's running React 17. Learn more: https://reactjs.org/link/switch-to-createroot"), !nv(t))
        throw new Error("Target container is not a DOM element.");
      {
        var i = gp(t) && t._reactRootContainer === void 0;
        i && S("You are calling ReactDOM.render() on a container that was previously passed to ReactDOMClient.createRoot(). This is not supported. Did you mean to call root.render(element)?");
      }
      return Zm(null, e, t, !1, a);
    }
    function Xx(e, t, a, i) {
      if (S("ReactDOM.unstable_renderSubtreeIntoContainer() is no longer supported in React 18. Consider using a portal instead. Until you switch to the createRoot API, your app will behave as if it's running React 17. Learn more: https://reactjs.org/link/switch-to-createroot"), !nv(a))
        throw new Error("Target container is not a DOM element.");
      if (e == null || !hy(e))
        throw new Error("parentComponent must be a valid React Component");
      return Zm(e, t, a, !1, i);
    }
    var aR = !1;
    function Zx(e) {
      if (aR || (aR = !0, S("unmountComponentAtNode is deprecated and will be removed in the next major release. Switch to the createRoot API. Learn more: https://reactjs.org/link/switch-to-createroot")), !nv(e))
        throw new Error("unmountComponentAtNode(...): Target container is not a DOM element.");
      {
        var t = gp(e) && e._reactRootContainer === void 0;
        t && S("You are calling ReactDOM.unmountComponentAtNode() on a container that was previously passed to ReactDOMClient.createRoot(). This is not supported. Did you mean to call root.unmount()?");
      }
      if (e._reactRootContainer) {
        {
          var a = gE(e), i = a && !Ao(a);
          i && S("unmountComponentAtNode(): The node you're attempting to unmount was rendered by another copy of React.");
        }
        return Xu(function() {
          Zm(null, null, e, !1, function() {
            e._reactRootContainer = null, JE(e);
          });
        }), !0;
      } else {
        {
          var u = gE(e), s = !!(u && Ao(u)), f = e.nodeType === qr && nv(e.parentNode) && !!e.parentNode._reactRootContainer;
          s && S("unmountComponentAtNode(): The node you're attempting to unmount was rendered by React and is not a top-level container. %s", f ? "You may have accidentally passed in a React root node instead of its container." : "Instead, have the parent component update its state and rerender in order to remove this component.");
        }
        return !1;
      }
    }
    br(Mx), xo(Ux), nh(zx), js(Ha), Id(Jv), (typeof Map != "function" || // $FlowIssue Flow incorrectly thinks Map has no prototype
    Map.prototype == null || typeof Map.prototype.forEach != "function" || typeof Set != "function" || // $FlowIssue Flow incorrectly thinks Set has no prototype
    Set.prototype == null || typeof Set.prototype.clear != "function" || typeof Set.prototype.forEach != "function") && S("React depends on Map and Set built-in types. Make sure that you load a polyfill in older browsers. https://reactjs.org/link/react-polyfills"), bc(eT), vy(qS, I1, Xu);
    function Jx(e, t) {
      var a = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : null;
      if (!Xm(t))
        throw new Error("Target container is not a DOM element.");
      return Nx(e, t, null, a);
    }
    function ek(e, t, a, i) {
      return Xx(e, t, a, i);
    }
    var SE = {
      usingClientEntryPoint: !1,
      // Keep in sync with ReactTestUtils.js.
      // This is an array for better minification.
      Events: [Ao, kf, Hh, mo, wc, qS]
    };
    function tk(e, t) {
      return SE.usingClientEntryPoint || S('You are importing createRoot from "react-dom" which is not supported. You should instead import it from "react-dom/client".'), Bx(e, t);
    }
    function nk(e, t, a) {
      return SE.usingClientEntryPoint || S('You are importing hydrateRoot from "react-dom" which is not supported. You should instead import it from "react-dom/client".'), Ix(e, t, a);
    }
    function rk(e) {
      return f_() && S("flushSync was called from inside a lifecycle method. React cannot flush when React is already rendering. Consider moving this call to a scheduler task or micro task."), Xu(e);
    }
    var ak = Px({
      findFiberByHostInstance: Xs,
      bundleType: 1,
      version: dE,
      rendererPackageName: "react-dom"
    });
    if (!ak && Nn && window.top === window.self && (navigator.userAgent.indexOf("Chrome") > -1 && navigator.userAgent.indexOf("Edge") === -1 || navigator.userAgent.indexOf("Firefox") > -1)) {
      var iR = window.location.protocol;
      /^(https?|file):$/.test(iR) && console.info("%cDownload the React DevTools for a better development experience: https://reactjs.org/link/react-devtools" + (iR === "file:" ? `
You might need to use a local HTTP server (instead of file://): https://reactjs.org/link/react-devtools-faq` : ""), "font-weight:bold");
    }
    Wa.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = SE, Wa.createPortal = Jx, Wa.createRoot = tk, Wa.findDOMNode = Gx, Wa.flushSync = rk, Wa.hydrate = qx, Wa.hydrateRoot = nk, Wa.render = Kx, Wa.unmountComponentAtNode = Zx, Wa.unstable_batchedUpdates = qS, Wa.unstable_renderSubtreeIntoContainer = ek, Wa.version = dE, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(new Error());
  }()), Wa;
}
function ER() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function")) {
    if (process.env.NODE_ENV !== "production")
      throw new Error("^_^");
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(ER);
    } catch (O) {
      console.error(O);
    }
  }
}
process.env.NODE_ENV === "production" ? (ER(), TE.exports = pk()) : TE.exports = vk();
var hk = TE.exports, bE, ey = hk;
if (process.env.NODE_ENV === "production")
  bE = ey.createRoot, ey.hydrateRoot;
else {
  var hR = ey.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
  bE = function(O, A) {
    hR.usingClientEntryPoint = !0;
    try {
      return ey.createRoot(O, A);
    } finally {
      hR.usingClientEntryPoint = !1;
    }
  };
}
const mk = "ringo_Header-module__root__-VrM-", yk = "ringo_Header-module__inner__-EltR", gk = "ringo_Header-module__hamburger__o7q7C", Sk = "ringo_Header-module__logo__QLIeK", Ek = "ringo_Header-module__searchSlot__cl4PT", Ck = "ringo_Header-module__right__v0ehG", _k = "ringo_Header-module__iconButton__9YN-6", Rk = "ringo_Header-module__alarmDot__d8UUL", Tk = "ringo_Header-module__mobileSearchBar__hWs8q", yl = {
  root: mk,
  inner: yk,
  hamburger: gk,
  logo: Sk,
  searchSlot: Ek,
  right: Ck,
  iconButton: _k,
  alarmDot: Rk,
  mobileSearchBar: Tk
}, bk = "ringo_Search-module__form__Pr9b3", wk = "ringo_Search-module__input__ug-ws", xk = "ringo_Search-module__button__c1eBr", ty = {
  form: bk,
  input: wk,
  button: xk
};
function Ga({
  name: O,
  inline: A = !0,
  "aria-hidden": T = !0
}) {
  return /* @__PURE__ */ X.jsx(
    "span",
    {
      className: "iconify",
      "data-icon": O,
      "data-inline": A ? "true" : "false",
      "aria-hidden": T
    }
  );
}
function mR({ placeholder: O }) {
  return /* @__PURE__ */ X.jsxs("form", { className: ty.form, method: "post", action: "/search", role: "search", children: [
    /* @__PURE__ */ X.jsx(
      "input",
      {
        className: ty.input,
        name: "search",
        placeholder: O,
        autoComplete: "off",
        type: "search"
      }
    ),
    /* @__PURE__ */ X.jsx("button", { type: "submit", formAction: "/goto", className: ty.button, "aria-label": "goto", children: /* @__PURE__ */ X.jsx(Ga, { name: "ic:round-find-in-page" }) }),
    /* @__PURE__ */ X.jsx("button", { type: "submit", formAction: "/search", className: ty.button, "aria-label": "search", children: /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-search" }) })
  ] });
}
function gl(O) {
  const A = document.querySelector(
    `meta[name="ringo-app:${O}"]`
  );
  return (A == null ? void 0 : A.content) ?? "";
}
function kk(O) {
  return gl(O) === "1";
}
function lv(O) {
  const A = document.getElementById(`ringo-app-island-${O}`);
  return (A == null ? void 0 : A.innerHTML) ?? "";
}
function Dk() {
  const O = document.getElementById("ringo-app-island-document-menu");
  if (!O)
    return [];
  const A = O.querySelectorAll("a[data-href]"), T = [];
  return A.forEach((oe) => {
    var ke;
    T.push({
      href: oe.dataset.href ?? "",
      label: ((ke = oe.textContent) == null ? void 0 : ke.trim()) ?? "",
      topic: oe.dataset.topic === "1"
    });
  }), T;
}
function Ok() {
  const O = document.getElementById("ringo-app-island-added-menu");
  if (!O)
    return [];
  const A = O.querySelectorAll("a[data-href]"), T = [];
  return A.forEach((oe) => {
    var ke;
    T.push({
      href: oe.dataset.href ?? "",
      label: ((ke = oe.textContent) == null ? void 0 : ke.trim()) ?? ""
    });
  }), T;
}
function Nk() {
  const O = document.getElementById("ringo-app-island-labels");
  if (!O)
    return {};
  const A = O.querySelectorAll("[data-key]"), T = {};
  return A.forEach((oe) => {
    const ke = oe.dataset.key;
    ke && (T[ke] = oe.textContent ?? "");
  }), T;
}
function Lk() {
  var T;
  const O = lv("sidebar-override"), A = ((T = document.getElementById("ringo-app-island-sidebar-override")) == null ? void 0 : T.dataset.empty) === "0";
  return {
    document: {
      title: gl("doc-title"),
      subTitle: gl("doc-sub-title"),
      lastEdit: gl("doc-last-edit"),
      viewCount: gl("doc-view-count"),
      lengthDoc: gl("doc-length")
    },
    user: {
      name: gl("user-name"),
      auth: gl("user-auth"),
      login: kk("user-login"),
      alarmCount: gl("user-alarm-count"),
      path: gl("user-path")
    },
    wiki: {
      wikiName: gl("wiki-name"),
      licenseHtml: lv("license")
    },
    menu: Dk(),
    addedMenu: Ok(),
    bodyHtml: lv("body"),
    preBodyHtml: lv("pre-body"),
    postBodyHtml: lv("post-body"),
    sidebar: A ? { mode: "override", html: O } : { mode: "default" },
    labels: Nk()
  };
}
function bt(O, A, T) {
  const oe = O[A];
  return oe && oe.trim() !== "" ? oe : T ?? A;
}
function Mk({ wikiName: O, user: A, labels: T, onMenu: oe }) {
  const ke = A.login && A.alarmCount && A.alarmCount !== "0", He = A.login ? "/user" : "/login";
  return /* @__PURE__ */ X.jsxs("header", { className: yl.root, id: "main", children: [
    /* @__PURE__ */ X.jsxs("div", { className: yl.inner, children: [
      /* @__PURE__ */ X.jsx(
        "button",
        {
          type: "button",
          className: yl.hamburger,
          onClick: oe,
          "aria-label": "open navigation",
          children: /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-menu" })
        }
      ),
      /* @__PURE__ */ X.jsx("a", { className: yl.logo, href: "/", children: O || "openNAMU Forge" }),
      /* @__PURE__ */ X.jsx("div", { className: yl.searchSlot, children: /* @__PURE__ */ X.jsx(mR, { placeholder: bt(T, "search") }) }),
      /* @__PURE__ */ X.jsxs("div", { className: yl.right, children: [
        /* @__PURE__ */ X.jsx(
          "a",
          {
            href: "/random",
            className: yl.iconButton,
            "aria-label": bt(T, "random"),
            title: bt(T, "random"),
            children: /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-shuffle" })
          }
        ),
        /* @__PURE__ */ X.jsx(
          "a",
          {
            href: "/recent_changes",
            className: yl.iconButton,
            "aria-label": bt(T, "recent_change"),
            title: bt(T, "recent_change"),
            children: /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-access-time" })
          }
        ),
        /* @__PURE__ */ X.jsx(
          "a",
          {
            href: He,
            className: `${yl.iconButton} ${ke ? yl.alarmDot : ""}`,
            "aria-label": A.login ? A.name : bt(T, "login"),
            title: A.login ? A.name : bt(T, "login"),
            children: /* @__PURE__ */ X.jsx(
              Ga,
              {
                name: A.login ? "ic:baseline-account-circle" : "ic:round-person-search"
              }
            )
          }
        )
      ] })
    ] }),
    /* @__PURE__ */ X.jsx("div", { className: yl.mobileSearchBar, children: /* @__PURE__ */ X.jsx(mR, { placeholder: bt(T, "search") }) })
  ] });
}
const Uk = "ringo_Drawer-module__backdrop__q3yl1", zk = "ringo_Drawer-module__backdropOpen__Svy4k", Ak = "ringo_Drawer-module__panel__s5wa6", jk = "ringo_Drawer-module__panelOpen__Q3dmW", Fk = "ringo_Drawer-module__head__K8RaX", Hk = "ringo_Drawer-module__headTitle__MYIhh", Vk = "ringo_Drawer-module__close__zbz-n", Pk = "ringo_Drawer-module__userCard__tSB93", Bk = "ringo_Drawer-module__userTop__j5Gwa", $k = "ringo_Drawer-module__avatar__V8GBD", Ik = "ringo_Drawer-module__userMeta__mtoYv", Yk = "ringo_Drawer-module__userName__evWO-", Qk = "ringo_Drawer-module__userSub__AyZqD", Wk = "ringo_Drawer-module__userActions__KL2Jv", Gk = "ringo_Drawer-module__userAction__tMD8d", qk = "ringo_Drawer-module__scroll__AOZHD", Kk = "ringo_Drawer-module__section__krMPR", Xk = "ringo_Drawer-module__sectionTitle__6BmH5", Zk = "ringo_Drawer-module__item__QRa4h", Jk = "ringo_Drawer-module__itemBadge__yS-NQ", Bn = {
  backdrop: Uk,
  backdropOpen: zk,
  panel: Ak,
  panelOpen: jk,
  head: Fk,
  headTitle: Hk,
  close: Vk,
  userCard: Pk,
  userTop: Bk,
  avatar: $k,
  userMeta: Ik,
  userName: Yk,
  userSub: Qk,
  userActions: Wk,
  userAction: Gk,
  scroll: qk,
  section: Kk,
  sectionTitle: Xk,
  item: Zk,
  itemBadge: Jk
};
function eD(O) {
  const A = (O || "").trim();
  return A ? A.charAt(0).toUpperCase() : "?";
}
function tD(O, A, T) {
  const oe = {
    title: bt(T, "list"),
    items: [
      {
        href: "/recent_changes",
        icon: "ic:baseline-autorenew",
        label: bt(T, "recent_change")
      },
      {
        href: "/recent_discuss",
        icon: "ic:baseline-add-comment",
        label: bt(T, "recent_discussion")
      },
      {
        href: "/vote",
        icon: "ic:baseline-how-to-vote",
        label: bt(T, "vote_list")
      },
      {
        href: "/bbs/main",
        icon: "ic:outline-developer-board",
        label: bt(T, "bbs_main")
      }
    ]
  }, ke = [
    {
      href: "/random",
      icon: "ic:baseline-shuffle",
      label: bt(T, "random")
    },
    {
      href: "/other",
      icon: "ic:baseline-build",
      label: bt(T, "other_tool")
    },
    {
      href: "/upload",
      icon: "ic:baseline-cloud-upload",
      label: bt(T, "upload")
    },
    {
      href: "/change/skin_set",
      icon: "ic:baseline-settings",
      label: bt(T, "skin_setting")
    }
  ];
  O.auth !== "0" && ke.splice(2, 0, {
    href: "/manager",
    icon: "ic:baseline-how-to-reg",
    label: bt(T, "admin_tool")
  });
  const He = {
    title: bt(T, "tool"),
    items: ke
  }, S = [
    {
      href: "/user",
      icon: "ic:baseline-account-box",
      label: bt(T, "user_tool")
    },
    {
      href: "/change",
      icon: "ic:baseline-manage-accounts",
      label: bt(T, "user_setting")
    }
  ];
  O.login && S.push(
    {
      href: "/alarm",
      icon: "ic:baseline-contact-mail",
      label: bt(T, "alarm"),
      badge: O.alarmCount && O.alarmCount !== "0" ? O.alarmCount : void 0
    },
    {
      href: "/watch_list",
      icon: "ic:round-preview",
      label: bt(T, "watchlist")
    },
    {
      href: "/star_doc",
      icon: "ic:twotone-stars",
      label: bt(T, "star_doc")
    }
  );
  const ft = {
    title: O.login ? O.name : bt(T, "user_tool"),
    items: S
  }, ee = [oe, He, ft];
  return A.length > 0 && ee.push({
    title: bt(T, "added_menu"),
    items: A.map((ne) => ({
      href: ne.href,
      icon: "ic:baseline-plus",
      label: ne.label
    }))
  }), ee;
}
function nD({
  open: O,
  onClose: A,
  wikiName: T,
  user: oe,
  addedMenu: ke,
  labels: He
}) {
  Qr.useEffect(() => (O ? document.body.classList.add("drawer-open") : document.body.classList.remove("drawer-open"), () => {
    document.body.classList.remove("drawer-open");
  }), [O]), Qr.useEffect(() => {
    if (!O)
      return;
    const Ve = (te) => {
      te.key === "Escape" && A();
    };
    return document.addEventListener("keydown", Ve), () => document.removeEventListener("keydown", Ve);
  }, [O, A]);
  const S = tD(oe, ke, He), ft = oe.path || "/", ee = oe.login && oe.alarmCount && oe.alarmCount !== "0", ne = oe.login && ee ? `${bt(He, "alarm")} ${oe.alarmCount}` : "";
  return /* @__PURE__ */ X.jsxs(X.Fragment, { children: [
    /* @__PURE__ */ X.jsx(
      "div",
      {
        className: `${Bn.backdrop} ${O ? Bn.backdropOpen : ""}`,
        onClick: A,
        "aria-hidden": "true"
      }
    ),
    /* @__PURE__ */ X.jsxs(
      "aside",
      {
        className: `${Bn.panel} ${O ? Bn.panelOpen : ""}`,
        role: "dialog",
        "aria-modal": "true",
        "aria-label": "navigation",
        "aria-hidden": !O,
        children: [
          /* @__PURE__ */ X.jsxs("div", { className: Bn.head, children: [
            /* @__PURE__ */ X.jsx("span", { className: Bn.headTitle, children: T || "openNAMU Forge" }),
            /* @__PURE__ */ X.jsx(
              "button",
              {
                type: "button",
                className: Bn.close,
                onClick: A,
                "aria-label": "close navigation",
                children: /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-close" })
              }
            )
          ] }),
          /* @__PURE__ */ X.jsxs("div", { className: Bn.userCard, children: [
            /* @__PURE__ */ X.jsxs("div", { className: Bn.userTop, children: [
              /* @__PURE__ */ X.jsx("span", { className: Bn.avatar, "aria-hidden": "true", children: eD(oe.name) }),
              /* @__PURE__ */ X.jsxs("div", { className: Bn.userMeta, children: [
                /* @__PURE__ */ X.jsx("div", { className: Bn.userName, children: oe.login ? oe.name : bt(He, "login") }),
                ne && /* @__PURE__ */ X.jsx("div", { className: Bn.userSub, children: ne })
              ] })
            ] }),
            /* @__PURE__ */ X.jsx("div", { className: Bn.userActions, children: oe.login ? /* @__PURE__ */ X.jsxs(
              "a",
              {
                className: Bn.userAction,
                href: `/logout?return=${encodeURIComponent(ft)}`,
                children: [
                  /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-logout" }),
                  bt(He, "logout")
                ]
              }
            ) : /* @__PURE__ */ X.jsxs(X.Fragment, { children: [
              /* @__PURE__ */ X.jsxs(
                "a",
                {
                  className: Bn.userAction,
                  href: `/login?return=${encodeURIComponent(ft)}`,
                  children: [
                    /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-login" }),
                    bt(He, "login")
                  ]
                }
              ),
              /* @__PURE__ */ X.jsxs(
                "a",
                {
                  className: Bn.userAction,
                  href: "/register",
                  children: [
                    /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-person-add-alt-1" }),
                    bt(He, "register")
                  ]
                }
              )
            ] }) })
          ] }),
          /* @__PURE__ */ X.jsx("div", { className: Bn.scroll, children: S.map((Ve, te) => /* @__PURE__ */ X.jsxs("div", { className: Bn.section, children: [
            Ve.title && /* @__PURE__ */ X.jsx("div", { className: Bn.sectionTitle, children: Ve.title }),
            Ve.items.map((me) => /* @__PURE__ */ X.jsxs(
              "a",
              {
                href: me.href,
                className: Bn.item,
                onClick: A,
                children: [
                  /* @__PURE__ */ X.jsx(Ga, { name: me.icon }),
                  /* @__PURE__ */ X.jsx("span", { children: me.label }),
                  me.badge && /* @__PURE__ */ X.jsx("span", { className: Bn.itemBadge, children: me.badge })
                ]
              },
              me.href + me.label
            ))
          ] }, Ve.title ?? te)) })
        ]
      }
    )
  ] });
}
const rD = "ringo_DocumentView-module__section__vcVB2", aD = "ringo_DocumentView-module__titleBlock__-1XR2", iD = "ringo_DocumentView-module__title__iMdAZ", lD = "ringo_DocumentView-module__subTitle__VZdFP", uD = "ringo_DocumentView-module__meta__C0v-2", oD = "ringo_DocumentView-module__metaItem__njgDo", sD = "ringo_DocumentView-module__menu__7dvZc", cD = "ringo_DocumentView-module__menuItem__04o89", fD = "ringo_DocumentView-module__menuItemActive__h8LBv", dD = "ringo_DocumentView-module__bodyShell__C9UTN", pD = "ringo_DocumentView-module__body__kNsGp", vD = "ringo_DocumentView-module__footer__wCcl8", hD = "ringo_DocumentView-module__footerLogo__-DjwS", wa = {
  section: rD,
  titleBlock: aD,
  title: iD,
  subTitle: lD,
  meta: uD,
  metaItem: oD,
  menu: sD,
  menuItem: cD,
  menuItemActive: fD,
  bodyShell: dD,
  body: pD,
  footer: vD,
  footerLogo: hD
};
function mD({
  document: O,
  menu: A,
  wiki: T,
  preBodyHtml: oe,
  bodyHtml: ke,
  postBodyHtml: He,
  labels: S
}) {
  const ft = O.subTitle && O.subTitle !== "0", ee = O.lastEdit && O.lastEdit !== "0";
  return /* @__PURE__ */ X.jsxs("section", { className: wa.section, children: [
    /* @__PURE__ */ X.jsxs("div", { className: wa.titleBlock, children: [
      /* @__PURE__ */ X.jsxs("h1", { className: wa.title, children: [
        /* @__PURE__ */ X.jsx("span", { children: O.title }),
        ft && /* @__PURE__ */ X.jsx("sub", { className: wa.subTitle, children: O.subTitle })
      ] }),
      ee && /* @__PURE__ */ X.jsxs("div", { className: wa.meta, children: [
        /* @__PURE__ */ X.jsxs("span", { className: wa.metaItem, children: [
          bt(S, "last_edit_time"),
          " : ",
          O.lastEdit
        ] }),
        O.viewCount && O.viewCount !== "0" && /* @__PURE__ */ X.jsxs("span", { className: wa.metaItem, children: [
          bt(S, "page_view"),
          " : ",
          O.viewCount
        ] }),
        O.lengthDoc && O.lengthDoc !== "" && /* @__PURE__ */ X.jsxs("span", { className: wa.metaItem, children: [
          bt(S, "length_doc"),
          " : ",
          O.lengthDoc
        ] })
      ] }),
      A.length > 0 && /* @__PURE__ */ X.jsx("div", { className: wa.menu, children: A.map((ne) => /* @__PURE__ */ X.jsx(
        "a",
        {
          href: ne.href,
          className: `${wa.menuItem} ${ne.topic ? wa.menuItemActive : ""}`,
          children: ne.label
        },
        ne.href + ne.label
      )) })
    ] }),
    /* @__PURE__ */ X.jsx("article", { className: wa.bodyShell, id: "main_data", children: /* @__PURE__ */ X.jsx(
      "div",
      {
        className: `${wa.body} opennamu_forge_main`,
        dangerouslySetInnerHTML: {
          __html: oe + ke + He
        }
      }
    ) }),
    /* @__PURE__ */ X.jsxs("footer", { className: wa.footer, id: "footer", children: [
      /* @__PURE__ */ X.jsx("div", { dangerouslySetInnerHTML: { __html: T.licenseHtml } }),
      /* @__PURE__ */ X.jsx("a", { className: wa.footerLogo, href: "https://github.com/opennamu-forge/opennamu-forge", children: /* @__PURE__ */ X.jsx("img", { alt: "opennamu-forge logo", src: "/views/main_css/file/s_logo.webp" }) })
    ] })
  ] });
}
const yD = "ringo_FloatingSidebar-module__root__dIfCn", gD = "ringo_FloatingSidebar-module__tabs__qLNFB", SD = "ringo_FloatingSidebar-module__tabButton__pUxP2", ED = "ringo_FloatingSidebar-module__tabButtonActive__MQ44W", CD = "ringo_FloatingSidebar-module__content__gFYu8", _D = "ringo_FloatingSidebar-module__override__TF1WT", Sl = {
  root: yD,
  tabs: gD,
  tabButton: SD,
  tabButtonActive: ED,
  content: CD,
  override: _D
};
function ry(O) {
  return O.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#x27;");
}
async function RD() {
  return (await (await fetch("/api/recent_change/10")).json()).filter((T) => T[6] === "").map((T) => `<a href="${`/w/${encodeURIComponent(T[1])}`}">${ry(T[1])}</a><br>${T[2]} | ${ry(T[3])}<br>`).join("");
}
async function TD() {
  return (await (await fetch("/api/recent_discuss/10")).json()).map((T) => `<a href="${`/thread/${encodeURIComponent(T[3])}`}">${ry(T[1])}</a><br>${T[2]} | ${T[5]}<br>`).join("");
}
async function bD() {
  const A = await (await fetch("/api/v2/bbs/main")).json();
  return ((A == null ? void 0 : A.data) ?? []).map(
    (oe) => `<a href="/bbs/w/${oe.set_id}/${oe.set_code}">${ry(oe.title)}</a><br>${oe.date} | ${oe.user_id}<br>`
  ).join("");
}
function wD({ labels: O }) {
  const [A, T] = Qr.useState(0), [oe, ke] = Qr.useState("Loading..."), He = Qr.useRef(["", "", ""]), S = Qr.useCallback(async (ee) => {
    const ne = He.current[ee];
    if (ne) {
      ke(ne);
      return;
    }
    ke("Loading...");
    try {
      const Ve = ee === 0 ? await RD() : ee === 1 ? await TD() : await bD();
      He.current[ee] = Ve || "", ke(Ve || "");
    } catch {
      ke("Error");
    }
  }, []);
  Qr.useEffect(() => {
    window.localStorage.getItem("main_css_off_sidebar") === "0" && S(0);
  }, [S]);
  const ft = Qr.useCallback(
    (ee) => {
      T(ee), S(ee);
    },
    [S]
  );
  return /* @__PURE__ */ X.jsxs("aside", { className: Sl.root, "aria-label": "document side panel", children: [
    /* @__PURE__ */ X.jsxs("div", { className: Sl.tabs, role: "tablist", children: [
      /* @__PURE__ */ X.jsx(
        "button",
        {
          type: "button",
          id: "side_button_1",
          role: "tab",
          "aria-selected": A === 0,
          className: `${Sl.tabButton} ${A === 0 ? Sl.tabButtonActive : ""}`,
          onClick: () => ft(0),
          children: bt(O, "edit")
        }
      ),
      /* @__PURE__ */ X.jsx(
        "button",
        {
          type: "button",
          id: "side_button_2",
          role: "tab",
          "aria-selected": A === 1,
          className: `${Sl.tabButton} ${A === 1 ? Sl.tabButtonActive : ""}`,
          onClick: () => ft(1),
          children: bt(O, "discussion")
        }
      ),
      /* @__PURE__ */ X.jsx(
        "button",
        {
          type: "button",
          id: "side_button_3",
          role: "tab",
          "aria-selected": A === 2,
          className: `${Sl.tabButton} ${A === 2 ? Sl.tabButtonActive : ""}`,
          onClick: () => ft(2),
          children: bt(O, "bbs")
        }
      )
    ] }),
    /* @__PURE__ */ X.jsx(
      "div",
      {
        id: "side_content",
        className: Sl.content,
        dangerouslySetInnerHTML: { __html: oe }
      }
    )
  ] });
}
function xD({ html: O }) {
  return /* @__PURE__ */ X.jsx(
    "aside",
    {
      className: `${Sl.root} ${Sl.override}`,
      dangerouslySetInnerHTML: { __html: O }
    }
  );
}
const kD = "ringo_QuickNav-module__root__TvRhS", DD = "ringo_QuickNav-module__button__svjH4", ny = {
  root: kD,
  button: DD
};
function OD() {
  return /* @__PURE__ */ X.jsxs("nav", { className: ny.root, id: "nav_bar", "aria-label": "quick navigation", children: [
    /* @__PURE__ */ X.jsx("a", { className: ny.button, href: "#main", id: "go_top", "aria-label": "go top", children: /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-arrow-upward" }) }),
    /* @__PURE__ */ X.jsx("a", { className: ny.button, href: "#footer", id: "go_bottom", "aria-label": "go bottom", children: /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-arrow-downward" }) }),
    /* @__PURE__ */ X.jsx("a", { className: ny.button, href: "#toc", id: "go_toc", "aria-label": "go toc", children: /* @__PURE__ */ X.jsx(Ga, { name: "ic:baseline-list" }) })
  ] });
}
function ND({ initial: O }) {
  const [A, T] = Qr.useState(!1), oe = Qr.useCallback(() => T(!0), []), ke = Qr.useCallback(() => T(!1), []), He = Qr.useMemo(() => O.sidebar.mode === "override" ? /* @__PURE__ */ X.jsx(xD, { html: O.sidebar.html }) : /* @__PURE__ */ X.jsx(wD, { labels: O.labels }), [O.labels, O.sidebar]);
  return /* @__PURE__ */ X.jsxs(X.Fragment, { children: [
    /* @__PURE__ */ X.jsx(
      Mk,
      {
        wikiName: O.wiki.wikiName,
        user: O.user,
        labels: O.labels,
        onMenu: oe
      }
    ),
    /* @__PURE__ */ X.jsx(
      nD,
      {
        open: A,
        onClose: ke,
        wikiName: O.wiki.wikiName,
        user: O.user,
        addedMenu: O.addedMenu,
        labels: O.labels
      }
    ),
    /* @__PURE__ */ X.jsx(
      mD,
      {
        document: O.document,
        menu: O.menu,
        wiki: O.wiki,
        preBodyHtml: O.preBodyHtml,
        bodyHtml: O.bodyHtml,
        postBodyHtml: O.postBodyHtml,
        labels: O.labels
      }
    ),
    He,
    /* @__PURE__ */ X.jsx(OD, {})
  ] });
}
function yR(O) {
  const A = new RegExp(`(?:^|; )${O}=([^;]*)`), T = document.cookie.match(A);
  return T ? T[1] : null;
}
function LD() {
  if (window.localStorage.getItem("main_css_use_sys_darkmode") !== "0") {
    const T = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches, oe = yR("main_css_darkmode");
    if (T && oe !== "1") {
      document.cookie = "main_css_darkmode=1; path=/", window.location.reload();
      return;
    }
    if (!T && oe === "1") {
      document.cookie = "main_css_darkmode=0; path=/", window.location.reload();
      return;
    }
  }
  yR("main_css_darkmode") === "1" ? document.documentElement.dataset.theme = "dark" : document.documentElement.dataset.theme = "light";
  const A = window.localStorage.getItem("main_css_fixed_width");
  if (A && A !== "") {
    const T = document.getElementById("ringo_add_style");
    T && (T.textContent += `
.ringo_section { max-width: ${A}px !important; }`);
  }
}
LD();
const MD = Lk(), gR = document.getElementById("ringo-app-root");
gR && bE(gR).render(
  /* @__PURE__ */ X.jsx(Qr.StrictMode, { children: /* @__PURE__ */ X.jsx(ND, { initial: MD }) })
);
