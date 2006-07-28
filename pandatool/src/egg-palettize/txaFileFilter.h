// Filename: txaFileFilter.h
// Created by:  drose (27Jul06)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) 2001 - 2004, Disney Enterprises, Inc.  All rights reserved
//
// All use of this software is subject to the terms of the Panda 3d
// Software license.  You should have received a copy of this license
// along with this source code; you will also find a current copy of
// the license at http://etc.cmu.edu/panda3d/docs/license/ .
//
// To contact the maintainers of this program write to
// panda3d-general@lists.sourceforge.net .
//
////////////////////////////////////////////////////////////////////

#ifndef TXAFILEFILTER_H
#define TXAFILEFILTER_H

#include "pandatoolbase.h"
#include "texturePoolFilter.h"

class TxaFile;

////////////////////////////////////////////////////////////////////
//       Class : TxaFileFilter
// Description : This is an abstract base class, a placeholder for any
//               number of different classes that may wish to
//               implement an effect on every texture loaded from disk
//               via the TexturePool.
//
//               In practice, as of the time of this writing, only the
//               TxaFileFilter (in pandatool) actually implements
//               this.  But other kinds of filters are possible.
//
//               This filter, once registered, will get a callback and
//               a chance to modify each texture as it is loaded from
//               disk the first time.  If more than one filter is
//               registered, each will be called in sequence, in the
//               order in which they were registered.  
//
//               The filter does not get called again if the texture
//               is subsequently reloaded from disk.  It is suggested
//               that filters for which this might be a problem should
//               call tex->set_keep_ram_image(true).
////////////////////////////////////////////////////////////////////
class EXPCL_PANDA TxaFileFilter : public TexturePoolFilter {
public:
  virtual PT(Texture) post_load(Texture *tex);

private:
  static void read_txa_file();

private:
  static TxaFile *_txa_file;
  static bool _got_txa_file;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TexturePoolFilter::init_type();
    register_type(_type_handle, "TxaFileFilter",
                  TexturePoolFilter::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "txaFileFilter.I"

#endif
