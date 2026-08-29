#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'results'
def j(n): return json.loads((R/n).read_text(encoding='utf-8'))
def close(a,b,tol=1e-9):
    if abs(a-b)>tol: raise AssertionError((a,b))
# Primary values cited in checkpoint
p=j('refahi_40_96_120_all.json'); close(p['models']['ridge']['M1_current']['r2'],0.1681167600952045); close(p['models']['ridge']['history_gain']['actual_delta_r2'],0.07061449907684869)
p=j('refahi_40_96_120_L1.json'); close(p['models']['ridge']['history_gain']['actual_delta_r2'],-0.0017297844804035067)
p=j('refahi_96_120_132_all.json'); close(p['models']['ridge']['history_gain']['actual_delta_r2'],0.013231502921979943)
p=j('refahi_96_120_132_L1.json'); close(p['models']['ridge']['M1_current']['r2'],0.5990869276144115); close(p['models']['extra_trees']['M1_current']['r2'],0.6299015909012915); close(p['models']['ridge']['history_gain']['actual_delta_r2'],-0.0003473036580003974)
# Calibrations cited in checkpoint
c=j('refahi_calibration_96_120_132_L1.json'); close(c['known_complete_null']['q95'],0.002594415962148216); close(c['known_incomplete_alt']['power_vs_null_q95'],0.99)
c=j('refahi_calibration_40_96_120_all.json'); close(c['known_complete_null']['q95'],0.015167879389329484)
print('REFAHI_CHECKPOINT_VALIDATED')
