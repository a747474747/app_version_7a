"""
Scenario Service - CRUD operations for financial scenarios.

This module provides the business logic for managing financial scenarios,
including creation, retrieval, updates, and deletion operations.
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from models.scenario import Scenario
from models.user_profile import UserProfile
from calculation_engine.schemas.calculation import CalculationState


class ScenarioService:
    """Service for managing financial scenarios."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def create_scenario(
        self,
        user_profile_id: int,
        name: str,
        created_by_clerk_id: str,
        description: Optional[str] = None
    ) -> Scenario:
        """
        Create a new scenario.

        Args:
            user_profile_id: ID of the user profile owning the scenario
            name: Human-readable name for the scenario
            description: Optional description
            created_by_clerk_id: Clerk ID of the user creating the scenario

        Returns:
            Created Scenario instance
        """
        # Generate unique scenario ID
        scenario_id = f"scenario_{uuid.uuid4().hex[:16]}"

        scenario = Scenario(
            scenario_id=scenario_id,
            name=name,
            description=description,
            user_profile_id=user_profile_id,
            status="DRAFT",
            version="1.0",
            mode="MODE-FACT-CHECK",
            created_by_clerk_id=created_by_clerk_id
        )

        self.db.add(scenario)
        self.db.commit()
        self.db.refresh(scenario)

        return scenario

    def get_scenario_by_id(self, scenario_id: str) -> Optional[Scenario]:
        """
        Retrieve a scenario by its unique ID.

        Args:
            scenario_id: Unique scenario identifier

        Returns:
            Scenario instance or None if not found
        """
        return self.db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()

    def get_scenarios_by_user(
        self,
        user_profile_id: int,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Scenario]:
        """
        Retrieve scenarios for a specific user.

        Args:
            user_profile_id: User profile ID
            status: Optional status filter
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of Scenario instances
        """
        query = self.db.query(Scenario).filter(Scenario.user_profile_id == user_profile_id)

        if status:
            query = query.filter(Scenario.status == status)

        return query.order_by(Scenario.updated_at.desc()).limit(limit).offset(offset).all()

    def update_scenario(
        self,
        scenario_id: str,
        updates: Dict[str, Any],
        updated_by_clerk_id: str
    ) -> Optional[Scenario]:
        """
        Update an existing scenario.

        Args:
            scenario_id: Unique scenario identifier
            updates: Dictionary of fields to update
            updated_by_clerk_id: Clerk ID of the user making the update

        Returns:
            Updated Scenario instance or None if not found
        """
        scenario = self.get_scenario_by_id(scenario_id)
        if not scenario:
            return None

        # Update allowed fields
        allowed_fields = {
            'name', 'description', 'status', 'version', 'calculation_state',
            'assumption_set', 'strategy_config', 'mode', 'projection_output',
            'last_calculated_at', 'tags', 'metadata'
        }

        for field, value in updates.items():
            if field in allowed_fields:
                setattr(scenario, field, value)

        # Update metadata
        scenario.updated_by_clerk_id = updated_by_clerk_id

        self.db.commit()
        self.db.refresh(scenario)

        return scenario

    def update_scenario_calculation_state(
        self,
        scenario_id: str,
        calculation_state: CalculationState,
        updated_by_clerk_id: str
    ) -> Optional[Scenario]:
        """
        Update a scenario's calculation state.

        Args:
            scenario_id: Unique scenario identifier
            calculation_state: New calculation state
            updated_by_clerk_id: Clerk ID of the user making the update

        Returns:
            Updated Scenario instance or None if not found
        """
        return self.update_scenario(
            scenario_id=scenario_id,
            updates={
                'calculation_state': calculation_state.model_dump(),
                'last_calculated_at': datetime.now().isoformat()
            },
            updated_by_clerk_id=updated_by_clerk_id
        )

    def update_scenario_projection_output(
        self,
        scenario_id: str,
        projection_output: Dict[str, Any],
        updated_by_clerk_id: str
    ) -> Optional[Scenario]:
        """
        Update a scenario's projection output.

        Args:
            scenario_id: Unique scenario identifier
            projection_output: New projection output data
            updated_by_clerk_id: Clerk ID of the user making the update

        Returns:
            Updated Scenario instance or None if not found
        """
        return self.update_scenario(
            scenario_id=scenario_id,
            updates={
                'projection_output': projection_output,
                'last_calculated_at': datetime.now().isoformat()
            },
            updated_by_clerk_id=updated_by_clerk_id
        )

    def delete_scenario(self, scenario_id: str, deleted_by_clerk_id: str) -> bool:
        """
        Soft delete a scenario by marking it as deleted.

        Args:
            scenario_id: Unique scenario identifier
            deleted_by_clerk_id: Clerk ID of the user deleting the scenario

        Returns:
            True if scenario was deleted, False if not found
        """
        scenario = self.get_scenario_by_id(scenario_id)
        if not scenario:
            return False

        # Soft delete - mark as deleted rather than actually deleting
        scenario.status = "DELETED"
        scenario.updated_by_clerk_id = deleted_by_clerk_id

        self.db.commit()

        return True

    def hard_delete_scenario(self, scenario_id: str) -> bool:
        """
        Permanently delete a scenario (hard delete).

        Args:
            scenario_id: Unique scenario identifier

        Returns:
            True if scenario was deleted, False if not found

        Note: This should only be used for cleanup/testing purposes
        """
        scenario = self.get_scenario_by_id(scenario_id)
        if not scenario:
            return False

        self.db.delete(scenario)
        self.db.commit()

        return True

    def search_scenarios(
        self,
        user_profile_id: int,
        query: str,
        limit: int = 20
    ) -> List[Scenario]:
        """
        Search scenarios by name or description.

        Args:
            user_profile_id: User profile ID to scope the search
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of matching Scenario instances
        """
        search_filter = f"%{query}%"
        return self.db.query(Scenario).filter(
            and_(
                Scenario.user_profile_id == user_profile_id,
                Scenario.status != "DELETED",
                or_(
                    Scenario.name.ilike(search_filter),
                    Scenario.description.ilike(search_filter)
                )
            )
        ).order_by(Scenario.updated_at.desc()).limit(limit).all()

    def get_scenario_count(self, user_profile_id: int, status: Optional[str] = None) -> int:
        """
        Get the count of scenarios for a user.

        Args:
            user_profile_id: User profile ID
            status: Optional status filter

        Returns:
            Number of scenarios
        """
        query = self.db.query(Scenario).filter(Scenario.user_profile_id == user_profile_id)

        if status:
            query = query.filter(Scenario.status == status)

        return query.count()

    def duplicate_scenario(
        self,
        scenario_id: str,
        new_name: str,
        duplicated_by_clerk_id: str
    ) -> Optional[Scenario]:
        """
        Create a duplicate of an existing scenario.

        Args:
            scenario_id: ID of scenario to duplicate
            new_name: Name for the new scenario
            duplicated_by_clerk_id: Clerk ID of the user duplicating

        Returns:
            New Scenario instance or None if original not found
        """
        original = self.get_scenario_by_id(scenario_id)
        if not original:
            return None

        # Create new scenario with copied data
        new_scenario = Scenario(
            scenario_id=f"scenario_{uuid.uuid4().hex[:16]}",
            name=new_name,
            description=original.description,
            user_profile_id=original.user_profile_id,
            status="DRAFT",
            version="1.0",
            calculation_state=original.calculation_state,
            assumption_set=original.assumption_set,
            strategy_config=original.strategy_config,
            mode=original.mode,
            tags=original.tags,
            metadata=original.metadata,
            created_by_clerk_id=duplicated_by_clerk_id
        )

        self.db.add(new_scenario)
        self.db.commit()
        self.db.refresh(new_scenario)

        return new_scenario


# Convenience function for getting a service instance
def get_scenario_service(db_session: Session) -> ScenarioService:
    """Factory function for ScenarioService."""
    return ScenarioService(db_session)
