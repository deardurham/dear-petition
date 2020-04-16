import React from 'react';
import PropTypes from 'prop-types';
import { DragNDropStyled } from './DragNDrop.styled';

function DragNDrop(props) {
  return (
    <DragNDropStyled>
      <p>DragNDrop</p>
    </DragNDropStyled>
  );
}

DragNDrop.propTypes = {};

DragNDrop.defaultProps = {};

export default DragNDrop;
