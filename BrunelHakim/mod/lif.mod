: ============================================================
: lif.mod  -  Leaky Integrate-and-Fire with stochastic drive
:
: Implements the Brunel & Hakim (1999) model equation:
:   tau * dV/dt = -V + muext + sigmaext * sqrt(tau) * xi
: where xi is Gaussian white noise (xi ~ N(0, 1/sqrt(dt))).
:
: Euler-Maruyama discretization (fixed dt):
:   V(t+dt) = V(t) + [(-V+muext)/tau]*dt + sigmaext*sqrt(dt/tau)*N(0,1)
:
: Design
: ------
:   INITIAL     : send a self-event (flag=1) at t=0 to bootstrap WATCH.
:   BREAKPOINT  : solve DERIVATIVE with euler for voltage integration.
:   DERIVATIVE  : LIF ODE + Gaussian noise (normrand); V' = 0 during refrac.
:   NET_RECEIVE :
:     flag == 1  bootstrap / post-spike: arm WATCH (V > theta) with flag 2.
:     flag == 2  WATCH fired: emit spike, reset V, re-arm WATCH.
:     flag == 0  external inhibitory spike: V += weight (if not refractory).
: ============================================================

NEURON {
    POINT_PROCESS LIF
    RANGE tau, theta, Vr, taurefr, muext, sigmaext
    RANGE V, refrac_end
}

PARAMETER {
    tau      = 20  (ms)   : membrane time constant
    theta    = 20  (mV)   : spike threshold
    Vr       = 10  (mV)   : reset potential
    taurefr  = 2   (ms)   : absolute refractory period
    muext    = 25  (mV)   : mean external drive (effective bias)
    sigmaext = 1   (mV)   : std dev of stochastic external drive
}

STATE {
    V (mV)
}

ASSIGNED {
    refrac_end (ms)
}

INITIAL {
    V          = Vr
    refrac_end = -1e9
    net_send(0, 1)   : bootstrap: enter NET_RECEIVE to arm WATCH
}

BREAKPOINT {
    SOLVE states METHOD euler
}

DERIVATIVE states {
    : Euler-Maruyama: deterministic drift + Gaussian noise kick.
    : During absolute refractoriness V is held constant.
    if (t > refrac_end) {
        V' = (-V + muext) / tau + (sigmaext / sqrt(tau * dt)) * normrand(0, 1)
    } else {
        V' = 0
    }
}

NET_RECEIVE(weight (mV)) {
    if (flag == 1) {
        : Bootstrap (t=0) or post-spike: arm threshold detector.
        WATCH (V > theta) 2

    } else if (flag == 2) {
        : Threshold crossing detected by WATCH.
        net_event(t)           : propagate spike to post-synaptic targets
        V          = Vr
        refrac_end = t + taurefr
        WATCH (V > theta) 2    : re-arm for the next spike

    } else {
        : Incoming inhibitory spike (flag == 0).
        : Directly shift membrane potential; ignored during refractoriness.
        if (t > refrac_end) {
            V = V + weight
        }
    }
}
