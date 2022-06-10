from copy import deepcopy

from flappy import models as flm

class ModelBook:
    """
    A collection of models, ready to use in run scripts.

    Parameters
    ----------
    ct_power_curve_file: str, optional
        The turbine curves file, forwarded to
        flappy.WS2PCT

    Attributes
    ----------
    amb_states_models: dict
        Dictionary of ambient states models
    rotor_models: dict
        Dictionary of rotor models
    turbine_models: dict
        Dictionary of turbine models
    turbine_orders: dict
        Dictionary of turbine orders
    controllers: dict
        Dictionary of controllers
    wake_models: dict
        Dictionary of wake models
    wake_superp: dict
        Dictionary of wake superposition models
    wake_frames: dict
        Dictionary of centre line models
    vert_profiles: dict
        Dictionary of vertical profile class names

    """

    def __init__(
            self, 
            ct_power_curve_file=None
        ):

        # define ambient states models:
        self.amb_states_models = {}

        # define rotor models:

        self.rotor_models = {}
        self.rotor_models['centre']  = flm.RMCentre()
        self.rotor_models['stencil'] = flm.RMStencil() 

        for n in range(3,13):
            self.rotor_models['ring' + str(n + 1)] = flm.RMRing(n=n)
        self.rotor_models['two_rings9']    = flm.RMRings(m=[4,4],angle0_deg=[45,0])
        self.rotor_models['two_rings13']   = flm.RMRings(m=[4, 8])
        self.rotor_models['three_rings19'] = flm.RMRings(m=[4,6,8])
        self.rotor_models['four_rings29'] = flm.RMRings(m=[4,6,8,10])
        for n in range(2,11):
            self.rotor_models['grid' + str(n*n)] = flm.RMGrid(n=n)
        self.rotor_models['grid400'] = flm.RMGrid(n=20)
        self.rotor_models['grid10000'] = flm.RMGrid(n=100)

        # define turbine models:
        self.turbine_models = {}
        if ct_power_curve_file is not None:
            self.turbine_models['ct_P_curves'] = flm.Ws2PCt(ct_power_curve_file=ct_power_curve_file)
        self.turbine_models['yaw2yawm']        = flm.Yaw2Yawm(ambient_wd=True, ambient_yaw=False)
        self.turbine_models['yawm2yaw']        = flm.Yawm2Yaw(ambient_wd=True, ambient_yaw=False)
        self.turbine_models['zeroOutsideFarm'] = flm.ZeroOutsideFarm()

        # define turbine orders:
        self.turbine_orders = {}
        self.turbine_orders['farm']       = flm.FarmTurbineOrder()
        self.turbine_orders['amb_wind']   = flm.WindTurbineOrder(use_amb=True)
        self.turbine_orders['wake_wind']  = flm.WindTurbineOrder(use_amb=False)
        self.turbine_orders['wake_frame'] = flm.WakeFrameTurbineOrder()

        # define controllers:
        self.controllers = {}
        self.controllers['default'] = flm.WTCDefault()

        # define wake models:
        self.wake_models = {}
        self.wake_models['Jensen']            = flm.WMJensen()
        self.wake_models['Jensen007']         = flm.WMJensen(k=0.07)
        self.wake_models['Frandsen']          = flm.WMFrandsen()
        self.wake_models['Bastankhah']        = flm.WMBastankhah()
        self.wake_models['Bastankhah_smear3'] = flm.WMBastankhah(delta_wd=3.)
        self.wake_models['PorteAgel']         = flm.WMPorteAgel()
        self.wake_models['Botasso']           = flm.WMBotasso()
        self.wake_models['Ishihara_wind']     = flm.WMIshiharaWind()
        self.wake_models['Ishihara_ti']       = flm.WMIshiharaTI()
        self.wake_models['IEC_TI_2005']       = flm.WMIECTI2005()
        self.wake_models['IEC_TI_2019']       = flm.WMIECTI2019()
        self.wake_models['CrespoHernandez']   = flm.WMTICrespoHernandez()

        # add nopartial-models:
        wmodels = list(self.wake_models.keys())
        for mname in wmodels:
            m = self.wake_models[mname]
            if m.partial_wakes:
                mname2 = mname + "_rotor"
                self.wake_models[mname2] = deepcopy(m)
                self.wake_models[mname2].partial_wakes = False

        # define induction models:
        #self.wake_models['Troldborg'] = flm.IMTroldborg()
        #self.wake_models['RankineHB'] = flm.IMRankineHB()
        #self.wake_models['VortexM']   = flm.IMVortexModel()
        
        # define wake superposition models:
        self.wake_superp = {}
        self.wake_superp['ti_linear']              = flm.TISuperpCollection(ti_superp='linear')
        self.wake_superp['ti_quadratic']           = flm.TISuperpCollection(ti_superp='quadratic')
        self.wake_superp['ti_max']                 = flm.TISuperpCollection(ti_superp='max')
        self.wake_superp['wind_linear']            = flm.WindSuperpLinear(use_ambws=False, limit_wake=False)
        self.wake_superp['wind_linear_amb']        = flm.WindSuperpLinear(use_ambws=True, limit_wake=False)
        self.wake_superp['wind_linear_lim']        = flm.WindSuperpLinear(use_ambws=False, limit_wake=True)
        self.wake_superp['wind_linear_amb_lim']    = flm.WindSuperpLinear(use_ambws=True, limit_wake=True)
        self.wake_superp['wind_quadratic']         = flm.WindSuperpQuadratic(use_ambws=False ,limit_wake=False)
        self.wake_superp['wind_quadratic_amb']     = flm.WindSuperpQuadratic(use_ambws=True, limit_wake=False)
        self.wake_superp['wind_quadratic_lim']     = flm.WindSuperpQuadratic(use_ambws=False, limit_wake=True)
        self.wake_superp['wind_quadratic_amb_lim'] = flm.WindSuperpQuadratic(use_ambws=True, limit_wake=True)
        self.wake_superp['wind_product']           = flm.WindSuperpProduct()

        # define wake centreline models:
        self.wake_frames = {}
        self.wake_frames['amb_wind']       = flm.AmbientWindFrame()
        self.wake_frames['rotor_wind']     = flm.RotorWindFrame()
        self.wake_frames['yaw_deflection'] = flm.YawDeflectionFrame()
        self.wake_frames['streamlines']    = flm.StreamlineFrame()

        # define farm calc data models:
        self.farm_calc_data_models = {}
        self.farm_calc_data_models['cables_mst'] = flm.CablesMST()

        # define vertical profiles:
        self.vert_profiles = {}
        self.vert_profiles['ws_abl_log_neutral']  = flm.vertical_profiles.ABLLogNeutralWsProfile.__name__
        self.vert_profiles['ws_abl_log_stable']   = flm.vertical_profiles.ABLLogStableWsProfile.__name__
        self.vert_profiles['ws_abl_log_unstable'] = flm.vertical_profiles.ABLLogUnstableWsProfile.__name__
        self.vert_profiles['ws_abl_log']          = flm.vertical_profiles.ABLLogWsProfile.__name__

    def __repr__(self):
        """
        The object's representation.
        
        Returns
        -------
        str:
            The object's representation
        
        """

        out = "Rotor models:"
        if len(self.rotor_models) == 0:
            out += "\n  (None)"
        else:
            for mname, m in self.rotor_models.items():
                out += "\n  " + mname + " -- " + str(m)

        out += "\nControllers:"
        if len(self.controllers) == 0:
            out += "\n  (None)"
        else:
            for mname, m in self.controllers.items():
                out += "\n  " + mname + " -- " + str(m)

        out += "\nTurbine models:"
        if len(self.turbine_models) == 0:
            out += "\n  (None)"
        else:
            for mname, m in self.turbine_models.items():
                out += "\n  " + mname + " -- " + str(m)

        out += "\nWake centreline models:"
        if len(self.wake_frames) == 0:
            out += "\n  (None)"
        else:
            for mname, m in self.wake_frames.items():
                out += "\n  " + mname + " -- " + str(m)

        out += "\nWake models:"
        if len(self.wake_models) == 0:
            out += "\n  (None)"
        else:
            for mname, m in self.wake_models.items():
                out += "\n  " + mname + " -- " + str(m)

        return out

    def reduce(self, wind_farm):
        """
        Return a reduced version,
        only carrying required models

        Parameters
        ----------
        wind_farm: flappy.WindFarm
            The wind farm
        
        Returns
        -------
        mbook: ModelBook
            The reduced model book

        """

        mbook = ModelBook()
        mbook.wake_superp = self.wake_superp
        mbook.turbine_orders = self.turbine_orders
        mtyps = ['rotor_models', 'turbine_models', 'controllers',
                'wake_models', 'wake_frames']
        ttyps = ['rotor_model', 'turbine_models', 'controller',
                'wake_models', 'wake_frame']
        for mi, mtyp in enumerate(mtyps):
            ttyp   = ttyps[mi]
            mdict0 = self.__dict__[mtyp]
            mdict  = {}
            for t in wind_farm.turbines:
                if ttyp == 'wake_models' or ttyp == 'turbine_models':
                    for wm in t.info[ttyp]:
                        if not wm in mdict:
                            mdict[wm] = mdict0[wm]
                else:
                    wm = t.info[ttyp]
                    if not wm in mdict:
                        mdict[wm] = mdict0[wm]

            mbook.__dict__[mtyp] = mdict
        
        return mbook
