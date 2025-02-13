import {
  Avatar,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  NavbarItem,
} from "@nextui-org/react";
import React, { useCallback } from "react";
import { DarkModeSwitch } from "./darkmodeswitch";
import { useRouter } from "next/navigation";
import { deleteAuthCookie } from "@/actions/auth.action";
import useSWR from "swr";

// A simple fetcher function that includes credentials.
const fetcher = (url: string) =>
  fetch(url, { credentials: "include" }).then((res) => {
    if (!res.ok) {
      throw new Error(`An error occurred: ${res.statusText}`);
    }
    return res.json();
  });

// Use an environment variable for the external API URL.
// Ensure NEXT_PUBLIC_API_URL is set in your .env file, e.g.:
// NEXT_PUBLIC_API_URL=https://api.prometheus.osn.wa.gov
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const UserDropdown = () => {
  const router = useRouter();

  // Fetch the current user info from your backend API.
  // The endpoint should return data like:
  // { username, upn, email, first_name, last_name }
  const { data: user } = useSWR(`${API_URL}/users/me`, fetcher);

  // Use a fallback if user data is not yet available.
  const displayUser = user || { username: "User", email: "" };

  const handleLogout = useCallback(async () => {
    await deleteAuthCookie();
    window.location.href = `${API_URL}/auth/login`;
  }, []);

  return (
    <Dropdown>
      <NavbarItem>
        <DropdownTrigger>
          <Avatar
            as="button"
            color="secondary"
            size="md"
            src="https://i.pravatar.cc/150?u=a042581f4e29026704d"
          />
        </DropdownTrigger>
      </NavbarItem>
      <DropdownMenu aria-label="User menu actions">
        <DropdownItem
          key="profile"
          className="flex flex-col justify-start w-full items-start"
        >
          <p>Signed in as</p>
          <p>{displayUser.username}</p>
        </DropdownItem>
        <DropdownItem key="settings">My Settings</DropdownItem>
        <DropdownItem key="team_settings">Team Settings</DropdownItem>
        <DropdownItem key="analytics">Analytics</DropdownItem>
        <DropdownItem key="system">System</DropdownItem>
        <DropdownItem key="configurations">Configurations</DropdownItem>
        <DropdownItem key="help_and_feedback">
          Help &amp; Feedback
        </DropdownItem>
        <DropdownItem
          key="logout"
          color="danger"
          className="text-danger"
          onPress={handleLogout}
        >
          Log Out
        </DropdownItem>
        <DropdownItem key="switch">
          <DarkModeSwitch />
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
};
